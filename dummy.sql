USE [GFSReporting]
GO
/****** Object:  StoredProcedure [pbi].[InboudConversionFunnelReport]    Script Date: 10/06/2025 02:12:05 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET NOCOUNT ON;
       
	   PRINT 'Populating InboudConversionFunnelReport ';
            IF OBJECT_ID(N'tempdb..#base') IS NOT NULL
                DROP TABLE #base;
            IF OBJECT_ID(N'tempdb..#base1') IS NOT NULL
                DROP TABLE #base1;
            IF OBJECT_ID(N'tempdb..#base1a') IS NOT NULL
                DROP TABLE #base1a;
            IF OBJECT_ID(N'tempdb..#base2') IS NOT NULL
                DROP TABLE #base2;
            IF OBJECT_ID(N'tempdb..#base2a') IS NOT NULL
                DROP TABLE #base2a;
            IF OBJECT_ID(N'tempdb..#base2b') IS NOT NULL
                DROP TABLE #base2b;
            IF OBJECT_ID(N'tempdb..#base3') IS NOT NULL
                DROP TABLE #base3;
            IF OBJECT_ID(N'tempdb..#base4') IS NOT NULL
                DROP TABLE #base4;
            IF OBJECT_ID(N'tempdb..#base5') IS NOT NULL
                DROP TABLE #base5;
            IF OBJECT_ID(N'tempdb..#LR') IS NOT NULL
                DROP TABLE #LR;
            IF OBJECT_ID(N'tempdb..#UW') IS NOT NULL
                DROP TABLE #UW;
            IF OBJECT_ID(N'tempdb..#Duration') IS NOT NULL
                DROP TABLE #Duration;
            IF OBJECT_ID(N'tempdb..#BaseSalesVariance') IS NOT NULL
                DROP TABLE #BaseSalesVariance;
            IF OBJECT_ID(N'tempdb..#SV1') IS NOT NULL
                DROP TABLE #SV1;
            IF OBJECT_ID(N'tempdb..#basefinal') IS NOT NULL
                DROP TABLE #basefinal;

            --Inbound Conversion Funnel base data from Fact ROI
            SELECT MonthStarting,
				   WeekStarting,
                   BrandId, 
                   ProductTypeID2, 
                   ProductType2 ProductType, 
                   ClientId, 
                   ISNULL(Response, 'n/a') Response, 
                   MAX(DateId) DateId, 
                   SUM(LeadsAllocated) Leads, 
                   userId
            INTO #base    --121876
            FROM HollardDW.dbo.FactROILeads a
                 LEFT JOIN HollardDW.dbo.DimDate x ON a.DateId = x.[Date]
            WHERE
             --MonthStarting BETWEEN DATEADD(month, DATEDIFF(month, 0, GETDATE()) - 13, 0) AND DATEADD(month, DATEDIFF(month, 0, GETDATE()) - 1, 0)
			 MonthStarting >= DATEADD(month, DATEDIFF(month, 0, GETDATE()) - 13, 0) 
            AND ChannelCategory = 'Inbound'
            AND ISNULL(Response, 'n/a') <> 'Referrals'
            GROUP BY MonthStarting,
					 WeekStarting,
                     BrandId, 
                     ProductTypeID2, 
                     ClientId, 
                     ProductType2, 
                     Response, 
                     userId
            ORDER BY 1;
         
		 
		 -- Delete the leads which are not needed

		 DELETE FROM #base
            WHERE leads = 0;
           
		   ---For MEdi and AHM STP and iSTP are not expcted hence deleting , Pat needs to look why these are populated
		   DELETE FROM #base
            WHERE brandid IN(3, 15)
            AND response LIKE '%stp%';
          

		  --update Brand Choosi for latest -1 to 0 
		  
		  UPDATE #base
              SET 
                  brandId = 0
            WHERE BrandId = -1;
         
		 
		 ---Check Sucessful contact to lead and replace the user in Base table , if not found keep original user from ROI 
		 
		 SELECT *
            INTO #base1
            FROM
            (
                SELECT DISTINCT 
                       a.MonthStarting,
					   a.WeekStarting,
                       a.BrandId, 
                       a.ProductTypeID2, 
                       a.ProductType, 
                       a.ClientId, 
                       a.Response, 
                       a.DateId, 
                       Leads, 
                       COALESCE(b.userId, a.userid) userId, 
                       ROW_NUMBER() OVER(PARTITION BY a.dateid, 
                                                      a.clientId
                       ORDER BY b.dtmInserted, 
                                leads DESC) RN,
                       CASE
                           WHEN b.ClientId IS NOT NULL
                           THEN a.Leads
                           ELSE 0
                       END Contacts
                FROM #base a
                     LEFT JOIN HollardDW.dbo.FactCCMSCallLogCTI b ON a.ClientId = b.ClientId
                                                                     AND a.BrandId = b.BrandID
                                                                     AND b.DateId BETWEEN a.DateId AND DATEADD(d, 7, a.DateId)
                                                                     AND ISNULL(b.CallOutcome, 'n/a') IN('SuccessfulContact', 'InboundCall')
                                                                     AND b.CallDuration >= 180
            ) a
            WHERE a.rn = 1;
        
		
		
		SELECT b.*, 
                   du.TeamName, 
                   du.TeamFunction, 
                   du.BusinessFunction, 
                   FullName
            INTO #base1a
            FROM #base1 b
                 LEFT JOIN HollardDW.dbo.DimUser du ON du.UserId = b.userId
                                                       AND b.DateId BETWEEN du.StartDate AND du.enddate;

            --Check Quotes 
            SELECT DISTINCT 
                   a.*,
                   CASE
                       WHEN b.ClientId IS NOT NULL
                       THEN a.Contacts
                       ELSE 0
                   END Quotes,
                   CASE
                       WHEN c.ClientId IS NOT NULL
                       THEN a.Contacts
                       ELSE 0
                   END Sales
            INTO #base2a
            FROM #base1a a
                 LEFT JOIN HollardDW.dbo.FactSalesActivity b ON a.ClientId = b.ClientId
                                                                AND a.BrandId = CASE
                                                                                    WHEN b.SourceSystemID = 2
                                                                                    THEN 0
                                                                                    ELSE b.BrandID
                                                                                END
                                                                AND b.DateId BETWEEN a.DateId AND DATEADD(d, 7, a.DateId)
                                                                AND ISNULL(b.UserId, 'n/a') NOT IN('OnlineUser', 'Web01', 'WebUser1', 'WebUser', 'HomeWeb01', 'LandlordsWeb01', 'MotorWeb01', 'TravelWeb01', 'ChoosiPetWeb01', 'ChoosiHealthWeb01', 'AffinityWeb01')  --MIGHT NEED TO ADD MORE FOR NON-AFFINITY
                 LEFT JOIN HollardDW.dbo.FactSalesActivity c ON a.ClientId = c.ClientId
                                                                AND a.BrandId = CASE
                                                                                    WHEN b.SourceSystemID = 2
                                                                                    THEN 0
                                                                                    ELSE b.BrandID
                                                                                END
                                                                AND c.DateId BETWEEN a.DateId AND DATEADD(d, 7, a.DateId)
                                                                AND ISNULL(c.UserId, 'n/a') NOT IN('OnlineUser', 'Web01', 'WebUser1', 'WebUser', 'HomeWeb01', 'LandlordsWeb01', 'MotorWeb01', 'TravelWeb01', 'ChoosiPetWeb01', 'ChoosiHealthWeb01', 'AffinityWeb01')  --MIGHT NEED TO ADD MORE FOR NON-AFFINITY
                                                                AND c.Sales > 0;

            --KOs
            SELECT DISTINCT 
                   a.*,
                   CASE
                       WHEN b.ClientId IS NOT NULL
                       THEN a.Contacts
                       ELSE 0
                   END Covid
            INTO #base2b
            FROM #base2a a
                 LEFT JOIN Evolve.dbo.tblCallLog b ON a.ClientId = b.ClientId
                                                      AND CAST(b.dtmInserted AS DATE) BETWEEN a.DateId AND DATEADD(d, 7, a.DateId)
                                                      AND ISNULL(b.UserId, 'n/a') NOT IN('OnlineUser', 'Web01', 'WebUser1', 'WebUser', 'HomeWeb01', 'LandlordsWeb01', 'MotorWeb01', 'TravelWeb01', 'ChoosiPetWeb01', 'ChoosiHealthWeb01', 'AffinityWeb01')  --MIGHT NEED TO ADD MORE FOR NON-AFFINITY
                                                      AND (b.Comments LIKE '%Deferred / Ineligible: Customer not eligible due to IP COVID screening%'
                                                           OR b.Comments LIKE '%Customer failed IP COVID screening%');

            --UW
            SELECT DISTINCT 
                   a.*,
                   CASE
                       WHEN b.ClientId IS NOT NULL
                       THEN a.Contacts
                       ELSE 0
                   END UWStart,
                   CASE
                       WHEN c.ClientId IS NOT NULL
                       THEN a.Contacts
                       ELSE 0
                   END UWAccepted,
                   CASE
                       WHEN d.ClientId IS NOT NULL
                       THEN a.Contacts
                       ELSE 0
                   END UWSale,
                   CASE
                       WHEN e.ClientId IS NOT NULL
                            AND d.ClientId IS NULL
                       THEN a.Contacts
                       ELSE 0
                   END UWNoSale,
                   CASE
                       WHEN f.ClientId IS NOT NULL
                            AND d.ClientId IS NULL
                            AND e.ClientId IS NULL
                       THEN a.Contacts
                       ELSE 0
                   END UWDecline
            INTO #base3
            FROM #base2b a
                 LEFT JOIN HollardDW.dbo.FactUWProcess b ON a.ClientId = b.ClientId
                                                            AND a.BrandId = CASE
                                                                                WHEN b.SourceSystemID = 2
                                                                                THEN 0
                                                                                ELSE b.BrandID
                                                                            END
                                                            AND CAST(b.InsertedDate AS DATE) BETWEEN a.DateId AND DATEADD(d, 7, a.DateId)
                                                            AND ISNULL(b.CreatedBy, 'n/a') NOT IN('OnlineUser', 'Web01', 'WebUser1', 'WebUser', 'HomeWeb01', 'LandlordsWeb01', 'MotorWeb01', 'TravelWeb01', 'ChoosiPetWeb01', 'ChoosiHealthWeb01', 'AffinityWeb01')  --MIGHT NEED TO ADD MORE FOR NON-AFFINITY
                 LEFT JOIN HollardDW.dbo.FactUWProcess c ON a.ClientId = c.ClientId
                                                            AND a.BrandId = CASE
                                                                                WHEN c.SourceSystemID = 2
                                                                                THEN 0
                                                                                ELSE c.BrandID
                                                                            END
                                                            AND CAST(c.InsertedDate AS DATE) BETWEEN a.DateId AND DATEADD(d, 7, a.DateId)
                                                            AND ISNULL(c.CreatedBy, 'n/a') NOT IN('OnlineUser', 'Web01', 'WebUser1', 'WebUser', 'HomeWeb01', 'LandlordsWeb01', 'MotorWeb01', 'TravelWeb01', 'ChoosiPetWeb01', 'ChoosiHealthWeb01', 'AffinityWeb01')  --MIGHT NEED TO ADD MORE FOR NON-AFFINITY
                                                            AND c.SystemSale + c.RUWSale + c.SystemNoSale + c.RUWNoSale > 0
                 LEFT JOIN HollardDW.dbo.FactUWProcess d ON a.ClientId = d.ClientId
                                                            AND a.BrandId = CASE
                                                                                WHEN d.SourceSystemID = 2
                                                                                THEN 0
                                                                                ELSE c.BrandID
                                                                            END
                                                            AND CAST(d.InsertedDate AS DATE) BETWEEN a.DateId AND DATEADD(d, 7, a.DateId)
                                                            AND ISNULL(d.CreatedBy, 'n/a') NOT IN('OnlineUser', 'Web01', 'WebUser1', 'WebUser', 'HomeWeb01', 'LandlordsWeb01', 'MotorWeb01', 'TravelWeb01', 'ChoosiPetWeb01', 'ChoosiHealthWeb01', 'AffinityWeb01')  --MIGHT NEED TO ADD MORE FOR NON-AFFINITY
                                                            AND d.SystemSale + d.RUWSale > 0
                 LEFT JOIN HollardDW.dbo.FactUWProcess e ON a.ClientId = e.ClientId
                                                            AND a.BrandId = CASE
                                                                                WHEN e.SourceSystemID = 2
                                                                                THEN 0
                                                                                ELSE e.BrandID
                                                                            END
                                                            AND CAST(e.InsertedDate AS DATE) BETWEEN a.DateId AND DATEADD(d, 7, a.DateId)
                                                            AND ISNULL(e.CreatedBy, 'n/a') NOT IN('OnlineUser', 'Web01', 'WebUser1', 'WebUser', 'HomeWeb01', 'LandlordsWeb01', 'MotorWeb01', 'TravelWeb01', 'ChoosiPetWeb01', 'ChoosiHealthWeb01', 'AffinityWeb01')
                                                            AND e.SystemNoSale + e.RUWNoSale > 0
                 LEFT JOIN HollardDW.dbo.FactUWProcess f ON a.ClientId = f.ClientId
                                                            AND a.BrandId = CASE
                                                                                WHEN f.SourceSystemID = 2
                                                                                THEN 0
                                                                                ELSE f.BrandID
                                                                            END
                                                            AND CAST(f.InsertedDate AS DATE) BETWEEN a.DateId AND DATEADD(d, 7, a.DateId)
                                                            AND ISNULL(f.CreatedBy, 'n/a') NOT IN('OnlineUser', 'Web01', 'WebUser1', 'WebUser', 'HomeWeb01', 'LandlordsWeb01', 'MotorWeb01', 'TravelWeb01', 'ChoosiPetWeb01', 'ChoosiHealthWeb01', 'AffinityWeb01')  --MIGHT NEED TO ADD MORE FOR NON-AFFINITY
                                                            AND f.SystemDecline + f.RUWDecline > 0;

            --Drop table #UW

            SELECT *, 
                   ROW_NUMBER() OVER(PARTITION BY InsertedDate, 
                                                  ClientId
                   ORDER BY InsertedDate, 
                            UWType DESC, 
                            ClientId) RN
            INTO #UW
            FROM
            (
                SELECT DISTINCT 
                       CAST(a.InsertedDate AS DATE) InsertedDate, 
                       'Referred to UW' UWType, 
                       clientId, 
                       createdby, 
                       a.BrandID, 
                       a.SourceSystemId --INTO #UW
                FROM HollardDW.dbo.FactUWProcess a
                     INNER JOIN HollardDW.dbo.DimBrand b ON a.BrandID = b.BrandID
                     LEFT JOIN HollardDW.dbo.DimResponse c ON a.ResponseID = c.ResponseID
                WHERE(a.RUWSale > 0
                      OR a.RUWDecline > 0
                      OR a.RUWNoSale > 0)
                    -- AND a.MonthStarting BETWEEN DATEADD(month, DATEDIFF(month, 0, GETDATE()) - 13, 0) AND DATEADD(month, DATEDIFF(month, 0, GETDATE()), 0)
					AND a.MonthStarting >= DATEADD(month, DATEDIFF(month, 0, GETDATE()) - 13, 0) 
            ) X;

            --	Sent to UW in seven days of post lead created
            --DROP table #base4
            SELECT *
            INTO #base4
            FROM
            (
                SELECT b.*, 
                       U.UWType, 
                       ROW_NUMBER() OVER(PARTITION BY b.dateid, 
                                                      b.clientId--, response
                       ORDER BY u.InsertedDate desc, 
                                b.leads) RN1, 
                       U.InsertedDate
                FROM #base3 b
                     LEFT JOIN #UW U ON U.ClientId = B.ClientID
                                        AND B.UserId = U.createdBy
                                        AND b.BrandId = CASE
                                                            WHEN U.SourceSystemID = 2
                                                            THEN 0
                                                            ELSE b.BrandID
                                                        END
                                        AND U.InsertedDate BETWEEN B.dateId AND CONVERT(DATE, DATEADD(dd, 7, B.dateId)) --AND CONVERT(DATE, L.dateid)
                --AND b.response = U.Response
                --   AND U.RN = 1;
            ) X
            WHERE RN1 = 1;

            --	Find duplicates with in same period and remove them
            --	DROP table #base5
            SELECT ROW_NUMBER() OVER(PARTITION BY InsertedDate, 
                                                  clientid
                   ORDER BY clientId, 
                            dateId desc) NearDate, 
                   *
            INTO #base5
            FROM #base4;



            UPDATE #base5
              SET 
                  RN1 = NULL, 
                  InsertedDate = NULL
            WHERE neardate >= 2;


            --	DROP table #Duration

            SELECT ClientId, 
                   UserId, 
                   DateId, 
                   Response, 
                   BrandId, 
                   ProductTypeId, 
                   SUM(Duration) Duration
            INTO #LR
            FROM DWResources.dbo.[vwLeadRankingLogWithMissingSales]--DWResources.dbo.tblLeadRankingLog 
            WHERE 
			--dtmInserted BETWEEN DATEADD(month, DATEDIFF(month, 0, GETDATE()) - 13, 0) AND DATEADD(month, DATEDIFF(month, 0, GETDATE()), 0)
			dtmInserted >= DATEADD(month, DATEDIFF(month, 0, GETDATE()) - 13, 0) 
            GROUP BY ClientId, 
                     UserId, 
                     DateId, 
                     Response, 
                     BrandId, 
                     ProductTypeId;

            -----DURATION
            --	DROP table #Duration
            SELECT b.NearDate, 
                   MonthStarting,
				   WeekStarting,
                   b.BrandId, 
                   ProductTypeID2, 
                   ProductType, 
                   b.ClientId, 
                   b.Response, 
                   b.DateId, 
                   Leads, 
                   b.userId, 
                   RN, 
                   Contacts, 
                   TeamName, 
                   TeamFunction, 
                   BusinessFunction, 
                   FullName, 
                   Quotes, 
                   Sales, 
                   Covid, 
                   UWStart, 
                   UWAccepted, 
                   UWSale, 
                   UWNoSale, 
                   UWDecline, 
                   UWType, 
                   RN1, 
                   InsertedDate, 
                   SUM(duration) duration
            --CASE
            --    WHEN neardate = 1
            --    THEN SUM(duration)
            --    ELSE 0
            --END duration
            INTO #Duration
            FROM #base5 B
                 LEFT JOIN #LR lr ON lr.UserId = B.UserId
                                     AND lr.dateID BETWEEN B.dateid AND CONVERT(DATE, DATEADD(dd, 7, B.DateId)) --AND CONVERT(DATE, L.dateid)
                                     AND lr.BrandID = B.BrandID
                                     AND lr.productTypeID = B.productTypeId2
                                     AND lr.Response = B.Response
                                     AND Lr.ClientId = B.clientID
            GROUP BY b.NearDate, 
                     MonthStarting,
					 WeekStarting, 
                     b.BrandId, 
                     ProductTypeID2, 
                     ProductType, 
                     b.ClientId, 
                     b.Response, 
                     b.DateId, 
                     Leads, 
                     b.userId, 
                     RN, 
                     Contacts, 
                     TeamName, 
                     TeamFunction, 
                     BusinessFunction, 
                     FullName, 
                     Quotes, 
                     Sales, 
                     Covid, 
                     UWStart, 
                     UWAccepted, 
                     UWSale, 
                     UWNoSale, 
                     UWDecline, 
                     UWType, 
                     RN1, 
                     InsertedDate
            ORDER BY clientid;

            --	DROP table #basefinal
            SELECT [MonthStarting],
				   WeekStarting,
                   b.[BrandId], 
                   [ProductTypeId2], 
                   [ProductType], 
                   b.ClientId,  -- Added ClientId
                   SUM([Leads]) [Leads], 
                   SUM([Contacts]) [Contacts], 
                   SUM([Quotes]) [Quotes], 
                   SUM(b.[Sales]) [Sales], 
                   SUM([Covid]) [Covid], 
                   SUM([UWStart]) [UWStart], 
                   SUM([UWAccepted]) [UWAccepted], 
                   SUM([UWSale]) [UWSale], 
                   SUM([UWNoSale]) [UWNoSale], 
                   SUM([UWDecline]) [UWDecline], 
                   b.Response, 
                   b.userId, 
                   TeamName, 
                   TeamFunction, 
                   BusinessFunction, 
                   FullName, 
                   SUM(B.Duration) Duration, 
                   COUNT(DISTINCT InsertedDate) ReferredToUW
            INTO #basefinal
            FROM #Duration B
            GROUP BY B.[MonthStarting],
					 WeekStarting,
                     B.[BrandId], 
                     [ProductTypeId2], 
                     [ProductType], 
                     B.ClientId,  -- Added ClientId
                     B.Response, 
                     B.userId, 
                     TeamName, 
                     TeamFunction, 
                     BusinessFunction, 
                     FullName;

            --	DROP table #SV1

            SELECT UserId, 
                   MonthStarting,
				   WeekStarting,
                   Response, 
                   BrandID,
                   --ClientId,  -- Added ClientId 
                   LeadWindowProductType, 
                   ProductTypeID, 
                   ISManager, 
                   SUM(Sales) Sales, 
                   SUM(PredSale) PredSale
            INTO #SV1
            FROM HollardDw.dbo.factsalesvariance s
                 LEFT JOIN hollarddw.dbo.dimbrand b ON(CASE
                                                           WHEN s.brand = 'Choosi'
                                                           THEN 'Multi'
                                                           ELSE s.brand
                                                       END) = b.brandName
                 LEFT JOIN evolve.dbo.tblproducttype pt ON s.LeadWindowProductType = Pt.productType
            WHERE dtmInserted >= DATEADD(month, DATEDIFF(month, 0, GETDATE()) - 13, 0) 
            GROUP BY UserId, 
                     MonthStarting,
					 WeekStarting,
                     Response, 
                     BrandId,
                     --ClientId,  -- Added ClientId
                     LeadWindowProductType, 
                     ProductTypeID, 
                     ISManager;

            --Drop table #BaseSalesVariance
            SELECT b.[MonthStarting],
				   b.WeekStarting, 
                   b.[BrandId], 
                   [ProductTypeId2], 
                   [ProductType], 
                   b.ClientId,  -- Added ClientId
                   [Leads], 
                   [Contacts], 
                   [Quotes], 
                   b.[Sales], 
                   [Covid], 
                   [UWStart], 
                   [UWAccepted], 
                   [UWSale], 
                   [UWNoSale], 
                   [UWDecline], 
                   b.Response, 
                   b.userId, 
                   TeamName, 
                   TeamFunction, 
                   BusinessFunction, 
                   FullName, 
                   ReferredToUW, 
                   SV.sales LRsales, 
                   SV.PredSale, 
                   SV.IsManager, 
                   Duration
            INTO #BaseSalesVariance
            FROM #basefinal B
                 LEFT JOIN #SV1 SV ON SV.UserId = B.UserId
                                      AND SV.WeekStarting = B.WeekStarting
                                      AND sv.BrandID = B.BrandID
                                      AND SV.productTypeID = B.productTypeId2
                                      AND SV.Response = B.Response
                                      --AND SV.ClientId = B.ClientId;  -- Added ClientId join condition

            -- Instead of truncating and inserting into permanent table, create a temp table with same structure
            IF OBJECT_ID(N'tempdb..#TblInboundFunnel') IS NOT NULL
                DROP TABLE #TblInboundFunnel;

            -- Create temp table structure explicitly
            CREATE TABLE #TblInboundFunnel (
                [MonthStarting] datetime,
                [WeekStarting] datetime,
                [BrandId] int,
                [BrandName] varchar(100),
                [ProductTypeId2] int,
                [ProductType] varchar(100),
                [ClientId] int,  -- Added ClientId
                [Leads] int,
                [Contacts] int,
                [Quotes] int,
                [Sales] int,
                [Covid] int,
                [UWStart] int,
                [UWAccepted] int,
                [UWSale] int,
                [UWNoSale] int,
                [UWDecline] int,
                [Response] varchar(100),
                [userId] varchar(50),
                [TeamName] varchar(100),
                [TeamFunction] varchar(100),
                [BusinessFunction] varchar(100),
                [FullName] varchar(100),
                [Duration] decimal(18,2),
                [LRsales] int,
                [PredSale] decimal(18,2),
                [ReferredToUW] int,
                [IsManager] bit
            );

            -- Insert data into temp table instead of production
            INSERT INTO #TblInboundFunnel
            ([MonthStarting],
			 [WeekStarting], 
             [BrandId], 
             [BrandName], 
             [ProductTypeId2], 
             [ProductType], 
             [ClientId],  -- Added ClientId
             [Leads], 
             [Contacts], 
             [Quotes], 
             [Sales], 
             [Covid], 
             [UWStart], 
             [UWAccepted], 
             [UWSale], 
             [UWNoSale], 
             [UWDecline], 
             [Response], 
             [userId], 
             [TeamName], 
             [TeamFunction], 
             [BusinessFunction], 
             [FullName], 
             [Duration], 
             [LRsales], 
             [PredSale], 
             [ReferredToUW], 
             [IsManager]
            )
                   SELECT MonthStarting,
						  WeekStarting, 
                          a.BrandId,
                          CASE
                              WHEN b.BrandName = 'multi'
                              THEN 'Choosi'
                              ELSE b.BrandName
                          END BrandName, 
                          a.ProductTypeId2, 
                          ProductType,
                          a.ClientId,  -- Added ClientId 
                          SUM(Leads) Leads, 
                          SUM(Contacts) Contacts, 
                          SUM(Quotes) Quotes, 
                          SUM(Sales) Sales, 
                          SUM(Covid) Covid, 
                          SUM(UWStart) UWStart, 
                          SUM(UWAccepted) UWAccepted, 
                          SUM(UWSale) UWSale, 
                          SUM(UWNoSale) UWNoSale, 
                          SUM(UWDecline) UWDecline, 
                          Response, 
                          userId, 
                          TeamName, 
                          TeamFunction, 
                          BusinessFunction, 
                          FullName, 
                          ISNULL(SUM(Duration), 0) Duration, 
                          SUM(LRsales) LRsales, 
                          SUM(PredSale) PredSale, 
                          SUM(ReferredToUW) ReferredToUW, 
                          ISManager
                   FROM #BaseSalesVariance a
                        INNER JOIN HollardDW.dbo.DimBrand b ON b.BrandID = a.brandid
                   WHERE [ProductTypeId2] IN(1, 2, 4, 5, 12)
                   GROUP BY MonthStarting,
							WeekStarting, 
                            a.BrandId, 
                            b.BrandName, 
                            ProductTypeId2, 
                            ProductType,
                            a.ClientId,  -- Added ClientId
                            Response, 
                            userId, 
                            TeamName, 
                            TeamFunction, 
                            BusinessFunction, 
                            FullName, 
                            ISManager;

---------------------------------------------------------------------------------------
---------------------------------- ANALYSIS QUERIES -----------------------------------
---------------------------------------------------------------------------------------

/*
Basic Query 1: Initial Data Validation
Purpose: Display all records from the temporary table to verify data is loaded correctly
This query is useful for debugging and initial data inspection
*/
SELECT * FROM #TblInboundFunnel;


select distinct clientid from hollarddw.dbo.factroileads where dateid >= '2025-01-01' and dateid < '2025-02-01'
and brandid =1 and producttypeid2=1


select distinct clientid from #TblInboundFunnel where 
monthstarting = '2025-01-01 00:00:00.000'
and brandname='Real' and producttype='Life'


select distinct f.clientid, t.leads, t.contacts, t.quotes, t.sales, t.covid, t.uwstart, t.uwaccepted, t.uwsale, t.uwnosale, t.uwdecline from hollarddw.dbo.factroileads f
left join #TblInboundFunnel t on f.clientid=t.clientid
where f.dateid >= '2025-01-01' and f.dateid < '2025-02-01'
and f.brandid =1 and f.producttypeid2=1
and t.monthstarting = '2025-01-01 00:00:00.000'
and t.brandname='Real' and t.producttype='Life'

---------------------------------------------------------------------------------------
---------------------------------- LEAD COMPARISON QUERIES -----------------------------------
---------------------------------------------------------------------------------------

-- 1. Count total leads in factroileads
SELECT *
into #factroijanleads
FROM hollarddw.dbo.factroileads 
WHERE dateid >= '2025-01-01' and dateid < '2025-02-01'
AND brandid =1 and producttypeid2=1; --16536 records

SELECT COUNT(DISTINCT clientid) AS TotalLeads FROM #factroijanleads; --9984 records

-- 2. Count leads in TblInboundFunnel
SELECT *
into #tblinboundfunneljanleads
FROM #TblInboundFunnel 
WHERE monthstarting = '2025-01-01 00:00:00.000'
AND brandname='Real' and producttype='Life'; --6612 records

SELECT COUNT(DISTINCT clientid) AS TotalInboundLeads FROM #tblinboundfunneljanleads; --6585 records

SELECT t.clientid
FROM #tblinboundfunneljanleads t
LEFT JOIN #factroijanleads f ON t.clientid = f.clientid
WHERE f.clientid IS NULL;

-- Create a new table to store the results
SELECT f.clientid,
       CASE 
           WHEN t.clientid IS NOT NULL THEN 'Present'
           ELSE 'Absent'
       END AS InInboundFunnel
INTO #FactROIWithInboundStatus
FROM #factroijanleads f
LEFT JOIN #tblinboundfunneljanleads t ON f.clientid = t.clientid;

-- Verify the results
SELECT * FROM #FactROIWithInboundStatus; --16626 records

-- Count the number of Present and Absent statuses
SELECT InInboundFunnel, COUNT(*) AS Count
FROM #FactROIWithInboundStatus
GROUP BY InInboundFunnel;
-- Present	12928
-- Absent	3698


-- Create a result table with one row per distinct clientid
SELECT f.clientid,
       CASE 
           WHEN t.clientid IS NOT NULL THEN 'Present'
           ELSE 'Absent'
       END AS InInboundFunnel
INTO #FactROIWithInboundStatusDistinct --10011 records
FROM (SELECT DISTINCT clientid FROM #factroijanleads) f
LEFT JOIN #tblinboundfunneljanleads t ON f.clientid = t.clientid;
/*
--In other words, if a clientid from #factroijanleads matches more than 
one row in #tblinboundfunneljanleads, then the left join will produce
multiple rows, which increases the total count in #FactROIWithInboundStatusDistinct.
*/

-- Verify the results by grouping
SELECT InInboundFunnel, COUNT(*) AS Count
FROM #FactROIWithInboundStatusDistinct
GROUP BY InInboundFunnel;
-- Present	6612
-- Absent	3399


select fd.ininboundfunnel, cl.*, s.*
from #FactROIWithInboundStatusDistinct fd
left join evolve.dbo.tblclient cl
on fd.clientid=cl.clientid
left join hollarddw.dbo.dimsource s
on cl.sourceid=s.sourceid
and s.brandid=1
and s.producttypeid=1
order by clientid

---------------------------------------------------------------------------------------
---------------------------------- INSIGHTS QUERIES ----------------------------------- 
---------------------------------------------------------------------------------------

-- -- Age Band Insights
-- SELECT 
--     AgeBand, 
--     InInboundFunnel, 
--     COUNT(*) AS TotalLeads
-- FROM
-- (
--     SELECT 
--          fd.ininboundfunnel,
--          CASE 
--              WHEN DATEDIFF(YEAR, cl.DOB, GETDATE()) < 30 THEN 'Under 30'
--              WHEN DATEDIFF(YEAR, cl.DOB, GETDATE()) BETWEEN 30 AND 39 THEN '30s'
--              WHEN DATEDIFF(YEAR, cl.DOB, GETDATE()) BETWEEN 40 AND 49 THEN '40s'
--              WHEN DATEDIFF(YEAR, cl.DOB, GETDATE()) BETWEEN 50 AND 59 THEN '50s'
--              ELSE '60+' 
--          END AS AgeBand
--     FROM #FactROIWithInboundStatusDistinct fd
--     LEFT JOIN evolve.dbo.tblclient cl
--         ON fd.clientid = cl.clientid
-- ) AS Derived
-- GROUP BY AgeBand, InInboundFunnel
-- ORDER BY AgeBand, InInboundFunnel;

-- -- Gender Insights
-- SELECT 
--     cl.Gender, 
--     fd.ininboundfunnel AS InboundStatus,
--     COUNT(*) AS TotalLeads
-- FROM #FactROIWithInboundStatusDistinct fd
-- LEFT JOIN evolve.dbo.tblclient cl
--     ON fd.clientid = cl.clientid
-- GROUP BY cl.Gender, fd.ininboundfunnel
-- ORDER BY cl.Gender, fd.ininboundfunnel;

-- -- State Insights
-- SELECT 
--     cl.State, 
--     fd.ininboundfunnel AS InboundStatus,
--     COUNT(*) AS TotalLeads
-- FROM #FactROIWithInboundStatusDistinct fd
-- LEFT JOIN evolve.dbo.tblclient cl
--     ON fd.clientid = cl.clientid
-- GROUP BY cl.State, fd.ininboundfunnel
-- ORDER BY cl.State, fd.ininboundfunnel;

-- -- Source Category Insights
-- SELECT 
--     s.sourcecategory, 
--     fd.ininboundfunnel AS InboundStatus,
--     COUNT(*) AS TotalLeads
-- FROM #FactROIWithInboundStatusDistinct fd
-- LEFT JOIN evolve.dbo.tblclient cl
--     ON fd.clientid = cl.clientid
-- LEFT JOIN hollarddw.dbo.dimsource s
--     ON cl.sourceid = s.sourceid
--        AND s.brandid = 1
--        AND s.producttypeid = 1
-- GROUP BY s.sourcecategory, fd.ininboundfunnel
-- ORDER BY s.sourcecategory, fd.ininboundfunnel;

-- -- IsResidentOfBrandCountryId Insights
-- SELECT 
--     cl.IsResidentOfBrandCountryId, 
--     fd.ininboundfunnel AS InboundStatus,
--     COUNT(*) AS TotalLeads
-- FROM #FactROIWithInboundStatusDistinct fd
-- LEFT JOIN evolve.dbo.tblclient cl
--     ON fd.clientid = cl.clientid
-- GROUP BY cl.IsResidentOfBrandCountryId, fd.ininboundfunnel
-- ORDER BY cl.IsResidentOfBrandCountryId, fd.ininboundfunnel;


drop table if exists #factroileads;
SELECT distinct dateid, clientid, brandid, sourceid, producttypeid2
into #factroileads
FROM hollarddw.dbo.factroileads 
WHERE dateid >= DATEADD(MONTH, -12, GETDATE())
AND dateid < GETDATE()
AND brandid =1 and producttypeid2=1; 

drop table if exists #funnel;
SELECT monthstarting, brandid, producttypeid2, producttype, clientid, leads, contacts, quotes, sales
into #funnel
FROM #TblInboundFunnel
where monthstarting >= DATEADD(MONTH, -12, GETDATE())
AND monthstarting < GETDATE()
and brandid =1 and producttypeid2=1;


select f.*, t.*, c.dob, c.gender, c.isresidentofbrandcountryid, 
c.state, s.sourcecategory from #factroileads f
left join #funnel t on f.clientid=t.clientid
AND CONVERT(VARCHAR(7), f.dateid, 120) = CONVERT(VARCHAR(7), t.monthstarting, 120)
left join evolve.dbo.tblclient c on f.clientid=c.clientid
left join hollarddw.dbo.dimsource s on f.sourceid=s.sourceid
AND s.brandid=1
AND s.producttypeid=1
