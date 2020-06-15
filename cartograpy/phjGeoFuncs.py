#####################################################################################
# 18 May 2020                                                                       #
# ===========                                                                       #
# The initial version of phjGeoFuncs.py created by combining two previous files,    #
# called phjShpFiles.py and point_in_polygon_012.py.                                #
#####################################################################################


# Some homegrown functions for dealing with .shp files
# ====================================================
# © Philip H. Jones, University of Liverpool, Apr 2015
#
# This home-made module contains functions to handle .shp files.
# In order to get Python to see the module, added following to .bash_profile or .bashrc:
#
# PYTHONPATH=$PYTHONPATH:/Users/phil/Dropbox/phjPythonModules; export PYTHONPATH
#
# To use the functions in this module, import phjShpFiles.
#
# Notes
# -----
# 1. phjConvertShpFileToCSV(path_and_name_of_shp_file,path_and_name_of_csv_file)
#
#    This function is used to convert a .shp file to a .csv file that can then be
# imported into a pandas dataframe. The reason that it doesn't import to a dataframe
# directly is that the process of reading in the .shp file can take a very long time. As
# a result, creating a csv file initially and then importing the csv data into a
# dataframe would probably be more efficient.
#
# To use this function:
#
# import phjShpFiles
# phjShpFiles.phjConvertShpFileToCSV('path_and_name_of_shp_file.shp','path_and_name_of_csv_file.csv')

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import fiona
import pandas	as pd
import numpy	as np
import pyproj
import pprint
import shapefile
import time
import pypyodbc
import phjShpFiles
import ast



class phjCounterError(Exception):
	# A description of how to define custom extensions is given at:
	# http://stackoverflow.com/questions/1877686/implementing-python-exceptions
	# This error exception is called when there is a problem with counting points
	# in a dataframe.
	def __init__(self,msg):
		self.msg = msg
	def __str__(self):
		return "ERROR: A counter error occurred. %s" % self.msg


class phjConvertPointToXandYError(Exception):
	# This error exception is called when there is a problem converting the point tuple
	# to x and y co-ordinates.
	def __init__(self,msg):
		self.msg = msg
	def __str__(self):
		return "ERROR: An error converting point tuple to coordinate values has occurred. %s" % self.msg


class phjNextPointError(Exception):
	# This error exception is called when there is a problem with creating the next point
	# in a dataframe.
	def __init__(self,msg):
		self.msg = msg
	def __str__(self):
		return "ERROR: An error creating the next point occurred. %s" % self.msg


class phjPolygonAreaError(Exception):
	# This error exception is called when there is a problem calculating the area of a
	# polygon.
	def __init__(self,msg):
		self.msg = msg
	def __str__(self):
		return "ERROR: An error while calculating the area of a polygon. %s" % self.msg


class phjShapesSummaryError(Exception):
	# This error exception is called when there is a problem summarising shape polygons.
	def __init__(self,msg):
		self.msg = msg
	def __str__(self):
		return "ERROR: An error while summarising shape polygons. %s" % self.msg


#########################################################################################
#
# IMPORTANT NOTICE
# ================
# Since version 010beta, this script has differed from previous versions in that the
# function phjConvertShpFileToCSV() was removed and saved as a more generic function
# in phjPythonModules where it can be imported and used by other scripts.
#
# In order to accommodate this change, the following changes were made:
#
# i.   phjConvertShpFileToCSV() was moved to a file called phjShpFiles and saved in
#      phjPythonModules.
# 
# ii.  phjConvertShpFileToCSV() originally defined the path and the name of the shp file
#      within the function. However, in the new version, the path and name of the shp
#      file is passed as a parameter, i.e.
#         phjConvertShpFileToCSV('path_and_name_of_shp_file.shp','path_and_name_of_csv_file.csv')
# 
# iii. As a consequence of ii above, the variable phjPathAndShpFilename is defined at
#      the top of the file.
#
# iv.  The new version of the function imports necessary libraries.
# 
# v.   In order to use the function, the function is imported using:
#         import phjShpFiles
#
# vi.  The function is called as:
#         phjShpFiles.phjConvertShpFileToCVS('path_and_name_of_shp_file.shp','path_and_name_of_csv_file.csv')
#
#########################################################################################
    
    
    
def phjPolygonDirection(phjPrintResults = False):
    return
    
    
    
def phjPolygonArea(phjPrintResults = False):
    return




def phjPointsInPolygon(phjPrintResults = False):
    phjPathAndShpFilename           = '/Users/philjones/Documents/Research/Mapping/Shapefiles/GB shapefiles combined/combined_gb_nuts_iii_EW2001_S2008/combined_gb_nuts_iii_EW2001_S2008.shp'
    phjPathAndShpFilePointsCSV      = '/Users/philjones/Documents/Research/Mapping/Shapefiles/GB shapefiles combined/combined_gb_nuts_iii_EW2001_S2008/combined_gb_nuts_iii_EW2001_S2008.csv'
    phjShpFilePointsCSVFilename     = 'phjShpFilePointsCSV.csv'
    phjPathToFiles                  = '/Users/philjones/Documents/Research/Hydatid/phj_new_analysis/'
    phjNUTS3LUTCSVFilename          = 'phjNUTS3LUTCSV.csv'
    phjPathAndNUTS3LUTCSV           = ''.join([phjPathToFiles,phjNUTS3LUTCSVFilename])
    phjReconstructCSVresponse       = ''

    print('POINT IN POLYGON')
    print('================\n')
    phjStartTime = time.time()
    print('Start time: {}'.format(phjStartTime))
    print('Path to default directory: {}'.format(phjPathToFiles))
    print('Path and filename of pre-saved CSV file: {}'.format(phjPathAndShpFilePointsCSV'))
    print('\n')

    while ((phjReconstructCSVresponse != 'y') & (phjReconstructCSVresponse != 'n')): 
        phjReconstructCSVresponse = raw_input('The data will be read from the pre-saved CSV file above unless you want to reconstruct the CSV file and save it in the default directory. This can take a LOOOOOOOONG time. Do you want to reconstruct the CSV file? (y/n) ')
        if phjReconstructCSVresponse == 'y':
            phjShpFiles.phjConvertShpFileToCSV(phjPathAndShpFilename,''.join([phjPathToFiles,phjShpFilePointsCSVFilename]))
            phjShpFilePointsDF = pd.read_csv(phjPathAndShpFilePointsCSV, index_col=0, converters={'point': ast.literal_eval}, dtype={'shape_number': np.int32, 'feature_number': np.int32, 'feature_id': np.int32, 'multipolygon_number': np.int32, 'polygon_number': np.int32, 'point_number': np.int32, 'clockwise': np.int32})
        elif phjReconstructCSVresponse == 'n':
            phjShpFilePointsDF = pd.read_csv(phjPathAndShpFilePointsCSV, index_col=0, converters={'point': ast.literal_eval}, dtype={'shape_number': np.int32, 'feature_number': np.int32, 'feature_id': np.int32, 'multipolygon_number': np.int32, 'polygon_number': np.int32, 'point_number': np.int32, 'clockwise': np.int32})
        else:
            print('Input not recognised. Please try again.\n')
    
    phjPrintDataframeDetails(phjShpFilePointsDF,'phjShpFilePointsDF','Database containing shapefile information')

    phjMovementPostcodesDF = phjGetMovementPostcodes()
    phjPrintDataframeDetails(phjMovementPostcodesDF, 'phjMovementPostcodesDF','Database of postcodes and coordinates of locations found in the cattle movement database')

    # phjPostcodeToNUTS3AreaLUT = phjDeterminePointsInPolygon(phjMovementPostcodes, phjShpFilePointsDF)
    phjDeterminePointsInPolygon(phjMovementPostcodesDF, phjShpFilePointsDF)

    # Save the dataframe as a .CSV file to save the hassle of re doing.
    phjMovementPostcodesDF.to_csv(phjPathAndNUTS3LUTCSV)

    phjEndTime = time.time()
    print('End time: {}'.format(phjEndTime))
    print('Total time taken (secs): {}'.format(phjEndTime-phjStartTime)
    print('ThE eNd')

    return



#########################
# Individual functions #
#######################

def phjPrintDataframeDetails(phjDF,
                             phjDFTitle,
                             phjDFDescription):
    print('Dataframe title: {}\n'.format(phjDFTitle))
    print('Description of dataframe: {}\n'.format(phjDFDescription))
    print('Number of records: {}\n'.format(len(phjDF)))
    print('Head records:\n{}\n'.format(phjDF.head(10)))
    print('dtypes:\n{}\n'.format(phjDF.dtypes))
    print('Variable names: {}\n'.format(phjDF.columns))
    
    return


def phjGetMovementPostcodes():
	##############################################################################
	# Create a dataframe containing all the postcodes and eastings and northings #
	# that need to be looked-up                                                  #
	##############################################################################
	
	phjMySQLConnection = pypyodbc.connect('DSN=hydatid_project_2012_update; UID=hydatid_user; PWD=abcd1234')
	
	# The following query selects all the unique locations that are referenced in the
	# movement database. The slightly complicated WHERE clause at the end of each SELECT
	# command simply ensures that records are only included if the postcode is present OR
	# both the x and y locations are present.
	phjMySQLQuery = "SELECT DISTINCT * \
					FROM \
						(SELECT \
							`hydatid_2012`.`phjMovements`.`OffLocationPostcode`					AS 'movement_postcode', \
							CAST(`hydatid_2012`.`phjMovements`.`OffLocationX` AS SIGNED)		AS 'location_x', \
							CAST(`hydatid_2012`.`phjMovements`.`OffLocationY` AS SIGNED)		AS 'location_y', \
							`NSPD`.`NSPDF_MAY_2010_UK_1M_FP`.`PCDS`								AS 'pcds', \
							CAST(`NSPD`.`NSPDF_MAY_2010_UK_1M_FP`.`OSEAST1M` AS SIGNED)			AS 'oseast1m', \
							CAST(`NSPD`.`NSPDF_MAY_2010_UK_1M_FP`.`OSNRTH1M` AS SIGNED)			AS 'osnrth1m', \
							`NSPD`.`NUTS3_names_and_codes_UK_as_at_12_03`.`NUTS303CD`			AS 'nuts303cd', \
							`NSPD`.`NUTS3_names_and_codes_UK_as_at_12_03`.`NUTS303NM`			AS 'nuts303nm' \
						FROM `hydatid_2012`.`phjMovements` \
							LEFT JOIN `NSPD`.`NSPDF_MAY_2010_UK_1M_FP` \
								ON `hydatid_2012`.`phjMovements`.`OffLocationPostcode` = `NSPD`.`NSPDF_MAY_2010_UK_1M_FP`.`PCDS` \
							LEFT JOIN `NSPD`.`NUTS3_names_and_codes_UK_as_at_12_03` \
								ON LEFT(`NSPD`.`NSPDF_MAY_2010_UK_1M_FP`.`NUTS`, 5) = `NSPD`.`NUTS3_names_and_codes_UK_as_at_12_03`.`NUTS303CD` \
						WHERE `hydatid_2012`.`phjMovements`.`OffLocationKey` IS NOT NULL \
							AND	`hydatid_2012`.`phjMovements`.`EartagWithoutSpaces` REGEXP '^UK' \
							AND (`hydatid_2012`.`phjMovements`.`OffLocationPostcode` IS NOT NULL \
								OR (CAST(`hydatid_2012`.`phjMovements`.`OffLocationX` AS SIGNED) IS NOT NULL \
									AND CAST(`hydatid_2012`.`phjMovements`.`OffLocationY` AS SIGNED) IS NOT NULL)) \
						UNION \
						SELECT \
							`hydatid_2012`.`phjMovements`.`OnLocationPostcode`					AS 'movement_postcode', \
							CAST(`hydatid_2012`.`phjMovements`.`OnLocationX` AS SIGNED)			AS 'location_x', \
							CAST(`hydatid_2012`.`phjMovements`.`OnLocationY` AS SIGNED)			AS 'location_y', \
							`NSPD`.`NSPDF_MAY_2010_UK_1M_FP`.`PCDS`								AS 'pcds', \
							CAST(`NSPD`.`NSPDF_MAY_2010_UK_1M_FP`.`OSEAST1M` AS SIGNED)			AS 'oseast1m', \
							CAST(`NSPD`.`NSPDF_MAY_2010_UK_1M_FP`.`OSNRTH1M` AS SIGNED)			AS 'osnrth1m', \
							`NSPD`.`NUTS3_names_and_codes_UK_as_at_12_03`.`NUTS303CD`			AS 'nuts303cd', \
							`NSPD`.`NUTS3_names_and_codes_UK_as_at_12_03`.`NUTS303NM`			AS 'nuts303nm' \
						FROM `hydatid_2012`.`phjMovements` \
							LEFT JOIN `NSPD`.`NSPDF_MAY_2010_UK_1M_FP` \
								ON `hydatid_2012`.`phjMovements`.`OnLocationPostcode` = `NSPD`.`NSPDF_MAY_2010_UK_1M_FP`.`PCDS` \
							LEFT JOIN `NSPD`.`NUTS3_names_and_codes_UK_as_at_12_03` \
								ON LEFT(`NSPD`.`NSPDF_MAY_2010_UK_1M_FP`.`NUTS`, 5) = `NSPD`.`NUTS3_names_and_codes_UK_as_at_12_03`.`NUTS303CD` \
						WHERE `hydatid_2012`.`phjMovements`.`OnLocationKey` IS NOT NULL \
							AND	`hydatid_2012`.`phjMovements`.`EartagWithoutSpaces` REGEXP '^UK' \
							AND (`hydatid_2012`.`phjMovements`.`OnLocationPostcode` IS NOT NULL \
								OR (CAST(`hydatid_2012`.`phjMovements`.`OnLocationX` AS SIGNED) IS NOT NULL \
								AND CAST(`hydatid_2012`.`phjMovements`.`OnLocationY` AS SIGNED) IS NOT NULL))) AS derived_table_alias \
						ORDER BY movement_postcode ASC"
		
	phjMySQLDF = pd.io.sql.read_sql(phjMySQLQuery,con=phjMySQLConnection)
	
	phjMySQLConnection.close()
	#
	# print phjMySQLDF
	#
	# ********** AT THIS POINT, SHOULD REPROJECT COORDINATES IF NECESSARY! **********
	#
	return phjMySQLDF


################################################
# Determine in which polygon the postcode sits #
################################################
def phjDeterminePointsInPolygon(phjMovementPostcodesDF,
                                phjShpFilePointsDF,
                                phjPrintResults = False):
	# This function assumes that the edges are defined as x1, y1 and x2, y2.
	#
	print 'Start phjDeterminePointsInPolygon() function.'
	print phjMovementPostcodesDF.head()
	print phjShpFilePointsDF.head()
	#
	phjMovementPostcodesDF['nuts3_label'] = np.nan
	phjMovementPostcodesDF['nuts3_name'] = np.nan
	#
	for i in range(len(phjMovementPostcodesDF)):
		phjShpFilePointsDF['adj_x1'] = np.nan
		phjShpFilePointsDF['adj_y1'] = np.nan
		phjShpFilePointsDF['adj_x2'] = np.nan
		phjShpFilePointsDF['adj_y2'] = np.nan
		#
		if	( ~np.isnan(phjMovementPostcodesDF['location_x'].iloc[i]) and ( ~np.isnan(phjMovementPostcodesDF['location_y'].iloc[i])) ):
			print phjMovementPostcodesDF['movement_postcode'].iloc[i]
			testPostcodeOSEAST1M = phjMovementPostcodesDF['location_x'].iloc[i]
			testPostcodeOSNRTH1M = phjMovementPostcodesDF['location_y'].iloc[i]
		elif ( ~np.isnan(phjMovementPostcodesDF['oseast1m'].iloc[i]) and ( ~np.isnan(phjMovementPostcodesDF['osnrth1m'].iloc[i])) ):
			print phjMovementPostcodesDF['movement_postcode'].iloc[i]
			testPostcodeOSEAST1M = phjMovementPostcodesDF['oseast1m'].iloc[i]
			testPostcodeOSNRTH1M = phjMovementPostcodesDF['osnrth1m'].iloc[i]
		else:
			testPostcodeOSEAST1M = np.nan
			testPostcodeOSNRTH1M = np.nan
			#
		if ( ~np.isnan(testPostcodeOSEAST1M) and ~np.isnan(testPostcodeOSNRTH1M) ):
			phjShpFilePointsDF['adj_x1'] = phjShpFilePointsDF['x1'] - testPostcodeOSEAST1M
			phjShpFilePointsDF['adj_y1'] = phjShpFilePointsDF['y1'] - testPostcodeOSNRTH1M
			phjShpFilePointsDF['adj_x2'] = phjShpFilePointsDF['x2'] - testPostcodeOSEAST1M
			phjShpFilePointsDF['adj_y2'] = phjShpFilePointsDF['y2'] - testPostcodeOSNRTH1M
			#
			# Originally tried to calculated slopes and intercepts on y and x axes for all 
			# edges. However, there were some potential issues with infinite values (either
			# infinite slope or infinite intercepts). Therefore, initially eliminate a large
			# number of edges based simply on signs of x and y coordinates.
			# The following expression returns True (i.e. edge NOT crossed) if the following
			# conditions are met:
			# i.  y1 and y2 are either both positive (or zero) or both negative (i.e. signbit
			#     state same for both)
			# ii. x1 and x2 are both negative (i.e. signbit turned on in both)
			phjInitialScreen =	( (np.signbit(phjShpFilePointsDF['adj_y1']) == np.signbit(phjShpFilePointsDF['adj_y2'])) |                          \
								  ((np.signbit(phjShpFilePointsDF['adj_x1']) == True) & (np.signbit(phjShpFilePointsDF['adj_x2']) == True)) )
			phjShpFilePointsDF['initial_screen'] = phjInitialScreen.astype(int)
			# If the egde doesn't cross the positive x axis, then we don't need to consider
			# those values:
			# Also, the shape file can list vertices for several polygons. If this is the 
			# case, the first polygon is the linear ring and subsequent polygons are holes.
			# Therefore, we can exclude any rows where polygon_number is greater than zero.
			# (N.B. If a hole in a polygon is defined, the same area will also be 
			# defined as a separate polygon with a different name and label).
			# Finally, when defining edges, if the final coordinate in the linear ring was
			# the same as the first coordinate then the value in the adjusted x2 and y2
			# coordinates were entered as NaN. Therefore, rows where both these values are
			# NaN can be excluded.
			phjReducedDataDF = phjShpFilePointsDF.ix[((phjShpFilePointsDF['initial_screen'] == 0) &                                                 \
													(phjShpFilePointsDF['polygon_number'] == 0) &                                                   \
													( ~np.isnan(phjShpFilePointsDF['adj_x2']) & ~np.isnan(phjShpFilePointsDF['adj_x2'])) ),         \
													['name','label','multipolygon_number','polygon_number','adj_x1','adj_y1','adj_x2','adj_y2']]
			# In the remaining edges, if adj_y1 is positive and adj_y2 is negative (or vice
			# versa) and both x values are positive then the edge crosses the positive x axis.
			# (Points where the x values are both negative have already been discarded.)
			# This calculation will take care of slightly awkward situations where the edge
			# is vertical (i.e. slope is infinite).
			phjCross = ( ((np.signbit(phjReducedDataDF['adj_x1']) == False ) & (np.signbit(phjReducedDataDF['adj_x2']) == False )) & \
						  (np.signbit(phjReducedDataDF['adj_y1']) != np.signbit(phjReducedDataDF['adj_y2'])) )
			# Convert those lines that do not cross to NaN rather than False...
			phjCross[phjCross==False] = np.nan
			# Add phjCross array to phjReducedDataDF dataframe...
			phjReducedDataDF['cross'] = phjCross
			#
			#For each edge, calculate slope and intercept (assuming x1 and x2 are different):
			phjReducedDataDF['slope'] = ( (phjReducedDataDF['adj_y2'] - phjReducedDataDF['adj_y1']) / (phjReducedDataDF['adj_x2'] - phjReducedDataDF['adj_x1']) ).where((phjReducedDataDF['adj_x1']) != (phjReducedDataDF['adj_x2']))
			phjReducedDataDF['intercept'] = ( phjReducedDataDF['adj_y1'] - (phjReducedDataDF['slope'] * phjReducedDataDF['adj_x1']) ).where((phjReducedDataDF['adj_x1']) != (phjReducedDataDF['adj_x2']))
			#
			# To determine if one of the edges with a slope crosses the positive x axis, we
			# need only compare the sign bit again. If the slope is positive and the
			# intercept is positive (or the slope is negative and the intercept is negative)
			# then the line can not possibly cross the positive x axis.
			# (N.B. The second parameter in the following .where clause is what to enter if
			# the condition is not true - in this case, leave what's already there. If this
			# parameter is not included then for cells where the condition is not true,
			# the value of phjReducedDataDF['cross'] is changed to NaN.)
			phjReducedDataDF['cross'] = (np.signbit(phjReducedDataDF['slope']) != np.signbit(phjReducedDataDF['intercept'])).where(np.isnan(phjReducedDataDF['cross']),phjReducedDataDF['cross'])
			# Remove edges that do not cross the positive x axis:
			phjReducedDataDF = phjReducedDataDF[phjReducedDataDF['cross'] == 1]
			# Calculate the position where the edge crosses the positive x axis. Firstly, if
			# line is vertical then enter value of adj_x1. If line is not vertical, calculate
			# place where edge crosses the positive x axis (and leave existing values alone
			# if condition not met).
			phjReducedDataDF['intercept_x'] = phjReducedDataDF['adj_x1'].where(phjReducedDataDF['adj_x1'] == phjReducedDataDF['adj_x2'])
			phjReducedDataDF['intercept_x'] = ((-1 * phjReducedDataDF['intercept']) / phjReducedDataDF['slope']).where((phjReducedDataDF['adj_x1'] != phjReducedDataDF['adj_x2']),phjReducedDataDF['intercept_x'])
			#
			# Now, split the database based on 'label' (and 'name') and add up the number
			# of 'crosses'. Then, work out if the sum of crosses is odd (i.e. inside
			# polygon) or even (i.e. outside polygon). Occasionally, it is possible that
			# a point will be inside 2 polygons (because one polygon is inside another). In
			# such cases, the polygon with the minimal value at which the line crosses the
			# x axis will be the polygon that contains the point.
			tempGrouped = phjReducedDataDF[['label','name','cross','intercept_x']].groupby(['label','name'],sort = False)
			tempResult = tempGrouped.agg({'intercept_x': np.amin, 'cross': np.sum})
			tempResult['inside'] = tempResult['cross'] % 2
			tempResult = tempResult[tempResult['inside'] == 1]
			tempResult.sort(['intercept_x'],ascending = True, inplace = True)
			tempResult.reset_index(inplace = True)
			print tempResult
			if len(tempResult.index) == 0:
				phjMovementPostcodesDF['nuts3_name'].iloc[i]  = np.nan
				phjMovementPostcodesDF['nuts3_label'].iloc[i] = np.nan
			else:
				phjMovementPostcodesDF['nuts3_name'].iloc[i]  = tempResult['name'].iloc[0]
				phjMovementPostcodesDF['nuts3_label'].iloc[i] = tempResult['label'].iloc[0]
			#
		else:
			phjMovementPostcodesDF['nuts3_name'].iloc[i]  = np.nan
			phjMovementPostcodesDF['nuts3_label'].iloc[i] = np.nan
	
	print 'End phjDeterminePointsInPolygon() function'
	
	return


if __name__ == "__main__":
	main()


##########
# The following is a brief example of how to add a tuple to a dataframe.
# The question was asked on StackOverflow 2015-01-15
# import pandas as pd
# import bumpy as np
# tempDF = pd.DataFrame({'miscdata': [1.2,3.2,4.1,2.3,3.3,2.5,4.3,2.5,2.2,4.2]})
# tempDF['newValue'] = np.nan
# tempDF['newTuple'] = np.nan
# "While NaN is the default missing value marker for reasons of computational speed and convenience, we need to be able to easily detect this value with data of different types: floating point, integer, boolean, and general object." (See: http://pandas.pydata.org/pandas-docs/stable/missing_data.html)
# When a new column is added and filled with NaNs, the dtype is set as float. In order to add a tuple, the dtype needs to be an object type. Therefore, change the dtype as follows:
# tempDF[['newValue','newTuple']] = tempDF[['newValue','newTuple']].astype(object)
# anyOldValue = 3.5
# for i in range(10):
#     tempDF.ix[(i,'newValue')] = anyOldValue
# 
# print tempDF
# anyOldTuple = (2.3,4.5)
# for i in range(10):
#     tempDF.set_value(i,'newTuple',anyOldTuple)
# 
# print tempDF
# z = tempDF.ix[(5,'newValue')]
# print z
# x, y = tempDF.ix[(5,'newTuple')]
# print x
# print y
##########


def phjConvertShpFileToCSV(phjShpPathAndFilename,phjCSVPathAndFilename):
	###########################################################
	# Create a dataframe containing the .shp file information #
	###########################################################
	# Read shp file details using fiona...
	with fiona.open(phjShpPathAndFilename, 'r') as phjShpFile:
		# Get coordinate reference system (CRS) details.
		phjShpFileCRS = phjShpFile.crs
		# phjSourceShpFile.crs is a dict of the shapefile parameters. Display a single
		# parameter value as follows:
		print phjShpFileCRS
		print 'Source shp file projection: ' + phjShpFileCRS['proj']
	
		# Could convert CRS details to a pandas dataframe as follows:
		# phjShpFileCRS_df = pd.DataFrame.from_dict(phjShpFileCRS, orient='index',
		# dtype = None)
		# phjShpFileCRS_df.rename(columns = {0: 'value'}, inplace = True)
		# Display values as follows:
		# print phjShpFileCRS_df
		# print phjShpFileCRS_df.dtypes
		# print phjShpFileCRS_df.loc['proj']
		
		# The structure of shapefiles
		# ===========================
		# The output from fiona is a Python ordered dict collection. Shapefiles have the
		# capacity to hold different types of geometry but the specification requires that
		# shapefiles contain only one type of geometry (e.g. polygons).
		# 
		# Structure of polygon geometry type
		# ----------------------------------
		# The coordinates section (see below) is a list of lists defining the exterior polygon
		# polygon (LinearRing) and any internal polygons ("holes") within the external polygon
		# (e.g. may represent a lake). Each off-shore island is a different feature.
		# The following shows how each feature is represented:
		#                                                               ONE AND ONLY POLYGON
		#                                                               WITH SINGLE HOLE
		# {'geometry': {'coordinates': [ [(co-ord_x1, co-ord_y1),   <-- Linear ring
		#                                 (co-ord_x2, co-ord_y2),
		#                                 (co-ord_x3, co-ord_y3),
		#                                 (co-ord_x4, co-ord_y4),
		#                                 (co-ord_x5, co-ord_y5)]
		#
		#                                [(co-ord_x6, co-ord_y6),   <-- hole (if present)
		#                                 (co-ord_x7, co-ord_y7),
		#                                 (co-ord_x8, co-ord_y8)] ],
		#               'type': 'Polygon'},
		#  'id': '1',
		#  'properties': OrderedDict([(u'NAME', u'Wales'), (u'LABEL', u'Wales')]),
		#  'type': 'Feature'}
		# 
		# Structure of a multipolygon geometry type
		# -----------------------------------------
		# In this case, multiple polygons are defined within each feature (rather then having
		# separate polygons defined as separate features as above).
		# Each feature will be represented as follows:
		#                                                                   POLYGON 1 WITH HOLE
		# {'geometry': {'coordinates': [ [ [(co-ord_x01, co-ord_y01),   <-- Linear ring
		#                                   (co-ord_x02, co-ord_y02),
		#                                   (co-ord_x03, co-ord_y03),
		#                                   (co-ord_x04, co-ord_y04),
		#                                   (co-ord_x05, co-ord_y05)]
		#
		#                                  [(co-ord_x06, co-ord_y06),   <-- hole (if present)
		#                                   (co-ord_x07, co-ord_y07),
		#                                   (co-ord_x08, co-ord_y08)] ]
		#                                                                   POLYGON 2 WITH HOLE
		#                                [ [(co-ord_x09, co-ord_y09),   <-- Linear ring
		#                                   (co-ord_x10, co-ord_y10),
		#                                   (co-ord_x11, co-ord_y11),
		#                                   (co-ord_x12, co-ord_y12),
		#                                   (co-ord_x13, co-ord_y13)]
		#
		#                                  [(co-ord_x14, co-ord_y14),   <-- hole (if present)
		#                                   (co-ord_x15, co-ord_y15),
		#                                   (co-ord_x16, co-ord_y16)] ] ],
		#               'type': 'MultiPolygon'},
		#  'id': '1',
		#  'properties': OrderedDict([(u'NAME', u'Scotland'), (u'LABEL', u'Scotland')]),
		#  'type': 'Feature'}
		#
		# To use phjReadPolygonPoints() function, pass the following variables:
		#     i. phjPolygonToRead = a tuple of tuples of coordinates (see above).
		#    ii. phjColumnNames = tuple of names of columns to be used in the dataframe.
		#   iii. phjFeatureNumber = integer representing the count of features read so far.
		#    iv. phjFeatureID = integer taken from feature['id'].
		#     v. phjFeatureName = string taken from feature['properties']['name'].
		#    vi. phjFeatureLabel = string taken from feature['properties']['label'].
		#   vii. phjGeomTypeName = string taken from feature['geometry']['type'] and is either
		#                          'Polygon' or 'MultiPolygon'.
		#  viii. phjMultipolgonNumber = integer representing the number of multipolygons read
		#                               or, in the case of polygon geometry type, equals 0.
		
		phjColumnNames = ['feature_number','feature_id','name','label','geom_type','multipolygon_number','polygon_number','point_number','point']
		phjShpFilePointsDF = pd.DataFrame(columns=phjColumnNames)
	
		# Step through each feature of the shapefile...
		phjFeatureNumber = 0
		for phjFeature in phjShpFile:
			print phjFeatureNumber, # Add comma to stop a carriage return being added
			print phjFeature['properties']['name'], '. ',
			phjID = phjFeature['id']
			if phjFeature['geometry']['type'] == 'Polygon':
				phjNextPolygonPointsDF = phjReadPolygonPoints( phjPolygonToRead = phjFeature['geometry']['coordinates'],
															   phjColumnNames = phjColumnNames,
															   phjFeatureNumber = phjFeatureNumber,
															   phjFeatureID = phjFeature['id'],
															   phjFeatureName = phjFeature['properties']['name'],
															   phjFeatureLabel = phjFeature['properties']['label'],
															   phjGeomTypeName = 'Polygon',
															   phjMultiPolygonNumber = 0	)
				# Concatenate the phjNextFeatureDF to the final dataframe
				phjShpFilePointsDF = pd.concat([phjShpFilePointsDF,phjNextPolygonPointsDF], axis=0, ignore_index=True)
			elif phjFeature['geometry']['type'] == 'MultiPolygon':
				# Step through each polygon in the multipolygon...
				phjMultiPolygonNumber = 0
				for phjMultiPolygon in phjFeature['geometry']['coordinates']:
					phjNextPolygonPointsDF = phjReadPolygonPoints( phjPolygonToRead = phjMultiPolygon,
																   phjColumnNames = phjColumnNames,
																   phjFeatureNumber = phjFeatureNumber,
																   phjFeatureID = phjFeature['id'],
																   phjFeatureName = phjFeature['properties']['name'],
																   phjFeatureLabel = phjFeature['properties']['label'],
																   phjGeomTypeName = 'MultiPolygon',
																   phjMultiPolygonNumber = phjMultiPolygonNumber	)
					# Concatenate the phjNextFeatureDF to the final dataframe
					phjShpFilePointsDF = pd.concat([phjShpFilePointsDF,phjNextPolygonPointsDF], axis=0, ignore_index=True)
					phjMultiPolygonNumber = phjMultiPolygonNumber + 1
			phjFeatureNumber = phjFeatureNumber + 1
	
	print phjShpFilePointsDF
	
	# Save the dataframe as a CSV file to save the hassle of re-doing.
	# One of the fields, namely 'point',is a tuple. When the tuple is read back into a 
	# dataframe using read_csv, the tuple is interpreted as as string. Regardless of how
	# the file is created (e.g. sep='\t' and quoting=None), reading the csv file back
	# always seems to interpret the tuple as a string.
	# An answer (accessed 1 Apr 2015) by DSM at:
	# http://stackoverflow.com/questions/23661583/reading-back-tuples-from-a-csv-file-with-pandas
	# provides a solution, namely include converters={"colA": ast.literal_eval}.
	# (!!! DO NOT USE EVAL() !!!)
	# However, DSM also recommends that storing tuples in a text file probably isn't a
	# great idea. So could convert the tuples to points before saving but the
	# ast.literal_eval option works OK for now.
	# However, as a 'belts-and-braces' approach, this function also converts the point
	# tuple to individual co-ordinates (x1 and y1) and calculates the next point to
	# define consecutive edges (x2 and y2).
	
	# Convert points to co-ordinates
	# ------------------------------
	try:
		phjShpFilePointsDF['x1'],phjShpFilePointsDF['y1'] = phjConvertPointTuplesToXandY(phjShpFilePointsDF['point'])
	except phjConvertPointToXandYError, e:
		print 'Error converting points to co-ordinate values: ', e
	except IndexError:
		print "An IndexError has occurred in phjConvertPointTuplesToXandY() function. This might indicate that the 'point' tuple has bene read from the csv file as a string rather than a tuple."
	
	# Add shape numbers
	# -----------------
	try:
		phjShpFilePointsDF['shape_number'] = phjAddShapeNumber(phjShpFilePointsDF['point_number'])
	except phjCounterError, e:
		print 'COUNTER ERROR: ', e
	
	
	# Add 'next point' field
	# ----------------------
	try:
		phjShpFilePointsDF['x2'] = phjDefineNextPoint(phjShpFilePointsDF, phjShpNumberName = 'shape_number', phjPointNumberName = 'point_number', phjCoordinateName = 'x1')
		phjShpFilePointsDF['y2'] = phjDefineNextPoint(phjShpFilePointsDF, phjShpNumberName = 'shape_number', phjPointNumberName = 'point_number', phjCoordinateName = 'y1')
	except phjNextPointError, e:
		print 'Error adding next point (or edges): ', e
	
	# Save dataframe to a csv file:
	phjShpFilePointsDF.to_csv(phjCSVPathAndFilename)

	# The CSV file produced above contains an unnamed column at the start to use as the index.
	# To create a dataframe containing values from this CSV file, use the following command:
	# >>> import ast
	# >>> phjShpFilePointsDF = pd.read_csv('phjShpFilePointsCSV.csv', index_col=0, converters={'point': ast.literal_eval}, dtype={'feature_number': np.int32, 'feature_id': np.int32, 'multipolygon_number': np.int32, 'polygon_number': np.int32, 'point_number': np.int32})

	print 'Basic csv file saved.'
	print 'Done!'
	
	return
	
	
def phjCreateShapesSummaryDF(phjCSVPathAndFilename,phjShapesSummaryCSVPathAndFilename):
	# Load CSV file of shape file created by phjConvertShpFileToCSV() function.
	# One of the fields, namely 'point',is a tuple. When the tuple is read back into a 
	# dataframe using read_csv, the tuple is interpreted as as string. Regardless of how
	# the file is created (e.g. sep='\t' and quoting=None), reading the csv file back
	# always seems to interpret the tuple as a string.
	# An answer (accessed 1 Apr 2015) by DSM at:
	# http://stackoverflow.com/questions/23661583/reading-back-tuples-from-a-csv-file-with-pandas
	# provides a solution, namely include converters={"colA": ast.literal_eval}.
	# (!!! DO NOT USE EVAL() !!! – it is a very dangerous function.)
	# However, DSM also recommends that storing tuples in a text file probably isn't a
	# great idea. So could convert the tuples to points before saving but the
	# ast.literal_eval option works OK for now.
	# So, to import this file into a dataframe, use:
	#     import ast
	#     phjShpFilePointsDF = pd.read_csv(phjCSVPathAndFilename, index_col=0, converters={'point': ast.literal_eval}, dtype={'feature_number': np.int32, 'feature_id': np.int32, 'multipolygon_number': np.int32, 'polygon_number': np.int32, 'point_number': np.int32})
	phjShpFilePointsDF = pd.read_csv(phjCSVPathAndFilename, index_col=0, converters={'point': ast.literal_eval}, dtype={'feature_number': np.int32, 'feature_id': np.int32, 'multipolygon_number': np.int32, 'polygon_number': np.int32, 'point_number': np.int32})
	
	# Add area of polygon
	# -------------------
	try:
		phjShpFilePointsDF['signed_area'],phjShpFilePointsDF['area'],phjShpFilePointsDF['clockwise'],phjShpFilePointsDF['centroidx'],phjShpFilePointsDF['centroidy'],phjShpFilePointsDF['momentx'],phjShpFilePointsDF['momenty'] = phjNewCalculatePolygonAreaPlus(phjShpFilePointsDF, phjShpNumberName = 'shape_number', phjVertex1XCoordinateName = 'x1',phjVertex1YCoordinateName = 'y1',phjVertex2XCoordinateName = 'x2',phjVertex2YCoordinateName = 'y2',phjReplaceExistingIntermediateValues = False)
	except phjPolygonAreaError, e:
		print 'Error occurred while calculating area of polygon.', e
	
	
	# Get shape based summary data
	# ----------------------------
	try:
		phjShapesSummaryDF = phjShapesSummary( phjShpFilePointsDF, phjShapeNumberName = 'shape_number', phjVariableNamesList = ['feature_number','feature_id','name','label','geom_type','multipolygon_number','polygon_number','signed_area','area','clockwise','centroidx','centroidy','momentx','momenty'] )
	except phjShapesSummaryError, e:
		print 'Error occurred while summarising shape polygons.', e
	
	# Save the final shape polygon summary dataframe as a CSV file
	phjShapesSummaryDF.to_csv(phjShapesSummaryCSVPathAndFilename)

	# The CSV file produced above contains an unnamed column at the start to use as the index.
	# To create a dataframe containing values from this CSV file, use the following command:
	# >>> phjShpFilePointsDF = pd.read_csv('phjShpFilePointsCSV.csv', index_col=0, dtype={'feature_number': np.int32, 'feature_id': np.int32, 'multipolygon_number': np.int32, 'polygon_number': np.int32, 'point_number': np.int32})

	print 'Shape summary CSV file saved.'
	print 'Done!'
	
	return phjShapesSummaryDF


#########################
# Individual functions #
#######################

def phjAddShapeNumber(phjDFVar):
	# This function labels each polygon shape with a number so that each polygon that
	# is defined has a unique label. It does this by stepping through each point in the
	# dataframe. The first point is zero and the shape number is labelled zero. As the
	# point number increases, the shape number remains the same. However, when the point
	# number returns to zero, the shape number increases by one.
	# For example:
	# 
	# point_number     shape_number
	#            0                0
	#            1                0
	#            2                0
	#            3                0
	#            4                0
	#            0                1
	#            1                1
	#            2                1
	#            3                1
	#            0                2
	#            1                2
	
	# This function should be passed a Pandas dataframe column, for example:
	# phjDF['point_number']
	
	phjOldArray = np.array(phjDFVar)
	phjArrayLength = len(phjOldArray)
	
	print phjOldArray
	
	# If first item in the array is NOT zero then raise an exception.
	if(phjOldArray[0] != 0):
		raise phjCounterError, 'The number of the first point was not equal to zero.'
	else:
		# Create an empty Numpy array (not zeroed to save time) to store the new data...
		phjNewArray = np.empty(phjArrayLength,dtype='int')
		
		# Set a counter to record the number of shapes so far encountered. Start at -1
		# so that when the first zero is encountered, the counter will be increased by 1
		# to the desired starting value of zero.
		phjShapeNumberCounter = -1
		
		# Step through each item in the array...
		for i in range(phjArrayLength):
			# print i
			if(phjOldArray[i] == 0):
				# When a new zero value is encountered, reset the point counter to zero
				# and increment the shape counter by one.
				phjPointNumberCounter = 0
				phjShapeNumberCounter += 1
				phjNewArray[i] = phjShapeNumberCounter
			else:
				# When the value in the old array is not equal to zero, increment the
				# point counter by 1. This counter should now equal the value in the array.
				# If it doesn't, then the original array  must have had some rows deleted.
				# In such a case, an exception should be raised. If all is fine, set the
				# value in the new array to be the shape counter.
				phjPointNumberCounter += 1
				if(phjOldArray[i] != phjPointNumberCounter):
					raise phjCounterError, 'There was a problem with the number of polygon points.'
				phjNewArray[i] = phjShapeNumberCounter
				
	return phjNewArray


def phjConvertPointTuplesToXandY(phjPointTuple):
	# This function takes a list of point tuples and converts it to two numpy arrays
	# representing x and y co-ordinates.
	#
	# ACCEPTS: An iterable list of point tuples (e.g. from a pandas dataframe).
	# RETURNS: A tuple of two numpy arrays representing X and Y co-ordinates.
	
	# Converting a pandas dataframe to a numpy array can be difficult. See hpaulj's
	# answer at:
	# http://stackoverflow.com/questions/29245187/accessing-the-first-items-in-a-numpy-array-of-tuples
	# ...basically, need to include .tolist() method.
	
	phjPointArray = np.array(phjPointTuple.tolist())
	
	return (phjPointArray[:,0],phjPointArray[:,1])


def phjDefineNextPoint(	phjDF,
						phjShpNumberName,
						phjPointNumberName,
						phjCoordinateName ):
	# Create a list of points offset by one (i.e. first point deleted and
	# others shifted up 1 position) to use as the second point that defines
	# each edge. If the first and last points are the same (i.e. the polygon
	# is closed then the final point should be NaN. If the first and last
	# point are not the same then the final point should be the same as the
	# first point. This is MUCH!!! faster than looping through each row.
	# For example:
	# 
	# 0   1.2         0   3.2
	# 1   3.2         1   2.5
	# 2   2.5   ==>   2   4.1
	# 3   4.1         3   3.3
	# 4   3.3         4   1.2
	# 5   1.2         5   NaN
	# 
	# The above algorithm needs to be done on vector of points for each polygon in turn.
	# Need to split-apply-combine based on 'shape number' variable. Initially, tried to
	# use groupby but it did not seem to be possible (or practical) to pass several
	# parameters to the fuction using apply(func). So, instead, stepped through each
	# shape number and created a temporary dataframe containing data for a single shape
	# only.
	
	phjLength = len(phjDF)
	phjOffset = np.zeros(phjLength)
	
	phjOffsetCounter = 0
	
	for i in pd.unique(phjDF[phjShpNumberName]):
		print 'Shape number: ', i
		phjGroupDF = phjDF.ix[phjDF[phjShpNumberName]==i,[phjShpNumberName,phjPointNumberName,phjCoordinateName]]
		print phjGroupDF
		phjGroupLength = len(phjGroupDF)
		
		# It is important that the shape number points are all consecutive and all in the
		# correct order. Several checks are made to ensure this is the case and errors
		# are raised if not.
		
		# The first point in the polygon needs to be a zero. If not, throw an error.
		# N.B. Originally tried to to use .ix format, such as:
		#    if(phjGroupDF.ix[0,phjPointNumberName] != 0):
		# However, it seems that .ix tries to index by label before trying to index by
		# position. So if the dataframe has an integer index which is not in sorted order
		# starting at zero, then using ix[i] will return the row labelled i rather than
		# the ith row. This will be the case where blocks of a dataframe are selected
		# and treated as a block without resetting the index. See answer by unutbu at:
		#    http://stackoverflow/com/questions/25254016/pandas-get-first-row-value-of-a-given-column
		# So, instead, use the iloc notation:
		if(phjGroupDF[phjPointNumberName].iloc[0] != 0):
			phjErrorString = 'The first point number of shape number %s is not equal to zero.' % i
			raise phjNextPointError, phjErrorString
		
		# The distance between the first and last points must be related to the length
		# of the vector.
		phjGroupFirstIndex = phjGroupDF.index[0]
		print 'Group first index: ', phjGroupFirstIndex
		phjGroupLastIndex = phjGroupDF.index[-1]
		print 'Group last indedx: ', phjGroupLastIndex
		if(phjGroupLastIndex - phjGroupFirstIndex != len(phjGroupDF) - 1):
			raise phjNextPointError, 'There is an inconsistency in the numbering of the index.'
		
		# The formula n(n+1)/2 can be used to sum n consecutive numbers starting at 1.
		# Hence, the sum of the shape point list should equal this formula. If not, then
		# there must be a mistake
		print 'Sum: ', phjGroupDF[phjPointNumberName].sum()
		print 'Sum (formula): ', ((phjGroupLength - 1) * phjGroupLength / 2)
		if(phjGroupDF[phjPointNumberName].sum() != ((phjGroupLength - 1) * phjGroupLength / 2)):
			raise phjNextPointError, 'Problem with numbering system.'
		
		# The offset values are, for the most part, the same as the main variable
		# but not including the first value.
		phjGroupOffset = np.zeros(phjGroupLength)
		phjGroupOffset[0:phjGroupLength - 1] = phjGroupDF[phjCoordinateName].iloc[1:]
		# The polygons defined in shapefile should be closed (i.e. the last point is
		# the same as the first point). If that is the case, then need to add a null
		# value as the final point in the 'next point' variable. If, however, the last
		# point is not a duplicate of the first point, then include the first point as
		# the final point of the 'next point' variable.
		if(phjGroupDF[phjCoordinateName].iloc[0] == phjGroupDF[phjCoordinateName].iloc[-1]):
			# Set the final element of the array to be NaN
			phjGroupOffset[-1] = np.nan
		else:
			# Otherwise, set the final element to be equal to the first element.
			phjGroupOffset[-1] = phjGroupDF[phjCoordinateName].iloc[0]
		
		# Transfer the phjGroupOffset values to the main phjOffset array:
		phjOffset[phjOffsetCounter:phjOffsetCounter + phjGroupLength] = phjGroupOffset
		
		phjOffsetCounter = phjOffsetCounter + phjGroupLength
		
	return phjOffset


def phjNewCalculatePolygonAreaPlus(	phjDF,
									phjShpNumberName,
									phjVertex1XCoordinateName,
									phjVertex1YCoordinateName,
									phjVertex2XCoordinateName,
									phjVertex2YCoordinateName,
									phjReplaceExistingIntermediateValues = False ):
	
	phjCalculateIntermediateVariables(	phjDF,
										phjVertex1XCoordinateName = 'x1',
										phjVertex1YCoordinateName = 'y1',
										phjVertex2XCoordinateName = 'x2',
										phjVertex2YCoordinateName = 'y2',
										phjReplaceExisting = phjReplaceExistingIntermediateValues )
	
	phjGroups = phjDF.groupby(phjShpNumberName)
	
	phjSignedArea = np.zeros(len(phjDF))
	phjCentroidX = np.zeros(len(phjDF))
	phjCentroidY = np.zeros(len(phjDF))
	phjMomentX = np.zeros(len(phjDF))
	phjMomentY = np.zeros(len(phjDF))
	
	phjAreaCounter = 0
	
	for phjGroupsName, phjGroupsGroup in phjGroups:
		phjTempGroupLength = len(phjGroupsGroup)
		phjTempSignedArea = ( phjGroupsGroup['__phjTempIntermediateVar1'].sum() ) / 2
		
		phjSignedArea[phjAreaCounter:phjAreaCounter + phjTempGroupLength]			= phjTempSignedArea
		
		phjCentroidX[phjAreaCounter:phjAreaCounter + phjTempGroupLength]	= (( phjGroupsGroup['__phjTempIntermediateVar2'].sum() ) / ( 6 * phjTempSignedArea ))
		phjCentroidY[phjAreaCounter:phjAreaCounter + phjTempGroupLength]	= (( phjGroupsGroup['__phjTempIntermediateVar3'].sum() ) / ( 6 * phjTempSignedArea ))
		
		# Not sure if this bit is right... but I think the 'moment' of each polygon
		# around the origin is the x centroid coordinate * the area of the polygon
		# (i.e. the area cancels out of the above calculation).
		phjMomentX[phjAreaCounter:phjAreaCounter + phjTempGroupLength]	= (( phjGroupsGroup['__phjTempIntermediateVar2'].sum() ) / 6 )
		phjMomentY[phjAreaCounter:phjAreaCounter + phjTempGroupLength]	= (( phjGroupsGroup['__phjTempIntermediateVar3'].sum() ) / 6 )
		
		phjAreaCounter = phjAreaCounter + phjTempGroupLength
	
	if(phjAreaCounter != len(phjDF)):
		raise phjPolygonAreaError, "Final area counter was incorrect in phjNewCalculatePolygonAreaPlus() function."
	
	print 'phjNewCalculatePolygonAreaPlus() function completed.'
	
	# Return results.
	# N.B. The sign of the signed area is the opposite to that calculated in the 
	# original phjCalculatePolygonArea() function.
	return ( phjSignedArea,
			 np.absolute(phjSignedArea),
			 np.signbit(phjSignedArea).astype(int),
			 phjCentroidX,
			 phjCentroidY,
			 phjMomentX,
			 phjMomentY)


def phjCalculateIntermediateVariables(	phjDF,
										phjVertex1XCoordinateName,
										phjVertex1YCoordinateName,
										phjVertex2XCoordinateName,
										phjVertex2YCoordinateName,
										phjReplaceExisting ):
	# The wikipedia entry on calculating the area of a polygon (see 
	# http://en.wikipedia.org/wiki/Centroid - accessed 28 Mar 2015) gave formulae
	# to calculate the X and Y coordinates of the centroid of the polygon. In so doing,
	# it was necessary to also calculate the signed area of the polygon. Consequently,
	# the area, direction and coordinates of the polygon can be calculated at the same
	# time using three variables that need to summed over each edge of the polygon.
	#
	#            n-1
	# A = 1/2 * sigma (x1*y2 - x2*y1)
	#            i=0	
	#
	#    Therefore, (x1*y2 - x2*y1) for each point is called __phjTempIntermediateVar1
	#
	#
	#              n-1
	# Cx = 1/6A * sigma (x1+x2)*(x1*y2 - x2*y1)
	#              i=0
	#
	#    Therefore, (x1+x2)*(x1*y2 - x2*y1) for each point is called __phjTempIntermediateVar2
	#
	#
	#              n-1
	# Cy = 1/6A * sigma (y1+y2)*(x1*y2 - x2*y1)
	#              i=0
	#
	#    Therefore, (y1+y2)*(x1*y2 - x2*y1) for each point is called __phjTempIntermediateVar3
	#
	# The above values are calculated for each point so they can be used to calculate
	# the area, direction and coordinates of the centroid.
	
	if phjReplaceExisting == True:
		phjDF['__phjTempIntermediateVar1'] = ((phjDF[phjVertex1XCoordinateName] * phjDF[phjVertex2YCoordinateName]) - (phjDF[phjVertex2XCoordinateName] * phjDF[phjVertex1YCoordinateName]))
		phjDF['__phjTempIntermediateVar2'] = (phjDF[phjVertex1XCoordinateName] + phjDF[phjVertex2XCoordinateName]) * phjDF['__phjTempIntermediateVar1']
		phjDF['__phjTempIntermediateVar3'] = (phjDF[phjVertex1YCoordinateName] + phjDF[phjVertex2YCoordinateName]) * phjDF['__phjTempIntermediateVar1']
	else:
		if '__phjTempIntermediateVar1' not in phjDF.columns:
			phjDF['__phjTempIntermediateVar1'] = ((phjDF[phjVertex1XCoordinateName] * phjDF[phjVertex2YCoordinateName]) - (phjDF[phjVertex2XCoordinateName] * phjDF[phjVertex1YCoordinateName]))
		
		if '__phjTempIntermediateVar2' not in phjDF.columns:
			phjDF['__phjTempIntermediateVar2'] = (phjDF[phjVertex1XCoordinateName] + phjDF[phjVertex2XCoordinateName]) * phjDF['__phjTempIntermediateVar1']
		
		if '__phjTempIntermediateVar3' not in phjDF.columns:
			phjDF['__phjTempIntermediateVar3'] = (phjDF[phjVertex1YCoordinateName] + phjDF[phjVertex2YCoordinateName]) * phjDF['__phjTempIntermediateVar1']
	
	return


def phjShapesSummary( phjDF,
					 phjShapeNumberName,
					 phjVariableNamesList):
	# Get a summary of everything based on each shape. Include a list of all the
	# relevant variable names (e.g. region name, signed area, area, clockwise, centroidx,
	# centroidy, momentx and momenty)
	
	phjShapesDF = phjDF.groupby(phjShapeNumberName)[phjVariableNamesList].first().reset_index()
	print phjShapesDF
	
	return phjShapesDF


########################################
# Unused or undefined (yet) functions #
######################################

def phjAddPolygonDirectionByCrossProducts(phjDF):
	# There is a method to calculate the direction of a polygon using the
	# cross-products of the vectors. However, the direction of a polygon is also
	# calculated as part of the signed area calculation in the phjCalculatePolygonArea()
	# function.
	print "The phjAddPolygonDirectionByCrossProducts() function is not yet implemented."
	return


def phjCrossProduct(phjDF):
	# Calculate the cross-product of each edge.
	print "The phjCrossProduct() function is not yet implemented."
	return


def phjCentreOfGravityOfMultiplePolygons(phjDF):
	# Many regions are made up of multiple individual polygons representing defined
	# mainland regions and multiple off-shore islands. To calculate the centre of
	# gravity of the whole region, calculate the average X (and Y) distances to each
	# polygon centroid, weighting by the area of each polygon. Need to confirm that this
	# works - but seems reasonable, doesn't it?
	print "Hello"
	return


def phjDoMiscellaneous():
	# The above code produces a Pandas dataframe that effectively lists each edge of the
	# polygon.
	# Now convert each item in each tuple to a separate column. Hopefully, this will
	# enable actions to be conducted on numpy arrays which should be faster.
	
	print 'Total number of vertices = ', len(phjShpFilePointsDF)
	
	# Create some empty lists that will be used to temporarily store the X and Y
	# co-ordinates before adding them to the dataframe above.
	phjTempX1 = []
	phjTempY1 = []
	phjTempX2 = []
	phjTempY2 = []
	
	for i in range(len(phjShpFilePointsDF)):
		phjConvertPointTupleToXandY(phjShpFilePointsDF.ix[i,'point'],phjTempX1,phjTempY1)
		phjConvertPointTupleToXandY(phjShpFilePointsDF.ix[i,'next_point'],phjTempX2,phjTempY2)
		if i % 1000 == 0:
			print '.',
	
	# Add lists of X and Y co-ordinates to dataframe
	phjPointLists = [phjTempX1,phjTempY1,phjTempX2,phjTempY2]
	phjPointListsNames = ['x1','y1','x1','y2']
	phjAddListsToDataFrame(phjShpFilePointsDF,phjPointLists,phjPointListsNames)
	

	# N.B. Apparently, can't use nan with integer arrays. Therefore, can't include
	# 'crossed': np.int8 in the above dict because all the vales in 'crossed' are, at the
	# moment, empty.
	
	return


def phjStepThroughShpFile(phjShpFile):
	# The output from fiona is a Python ordered dict collection. The structure is
	# described in more detail in the function phjReadPolygonPoints().
	#
	# Step through each feature of the shapefile...if you want to:
	for phjFeature in phjShpFile:
		phjID = phjFeature['id']
		if phjFeature['geometry']['type'] == 'Polygon':
			# Step through each polygon (LinearRing and holes)...
			for phjPolygon in phjFeature['geometry']['coordinates']:
				# Step through each point of each polygon...
				for phjPoint in phjPolygon:
					phjLong, phjLat = phjPoint
					# print phjID, phjLong, phjLat
		elif phjFeature['geometry']['type'] == 'MultiPolygon':
			# Step through each polygon in the multipolygon...
			for phjMultiPolygon in phjFeature['geometry']['coordinates']:
				# ...and then through each polygon (LinearRing and holes)...
				for phjPolygon in phjMultiPolygon:
					for phjPoint in phjPolygon:
						phjLong, phjLat = phjPoint
						# print phjID, phjLong, phjLat
	
	# Pretty print the first feature as an example, if so desired...
	pprint.pprint(phjShpFile[0])
		
	# As an example, print the name of the area...
	print phjShpFile[0]['properties']['name']
	
	return


def phjReadPolygonPoints( phjPolygonToRead,
						  phjColumnNames,
						  phjFeatureNumber,
						  phjFeatureID,
						  phjFeatureName,
						  phjFeatureLabel,
						  phjGeomTypeName,
						  phjMultiPolygonNumber ):

	# The structure of shapefiles
	# ===========================
	# The output from fiona is a Python ordered dict collection. Shapefiles have the
	# capacity to hold different types of geometry but the specification requires that
	# shapefiles contain only one type of geometry (e.g. polygons).
	# 
	# Structure of polygon geometry type
	# ----------------------------------
	# The coordinates section (see below) is a list of lists defining the exterior polygon
	# polygon (LinearRing) and any internal polygons ("holes") within the external polygon
	# (e.g. may represent a lake). Each off-shore island is a different feature.
	# The following shows how each feature is represented:
	#                                                               ONE AND ONLY POLYGON
	#                                                               WITH SINGLE HOLE
	# {'geometry': {'coordinates': [ [(co-ord_x1, co-ord_y1),   <-- Linear ring
	#                                 (co-ord_x2, co-ord_y2),
	#                                 (co-ord_x3, co-ord_y3),
	#                                 (co-ord_x4, co-ord_y4),
	#                                 (co-ord_x5, co-ord_y5)]
	#
	#                                [(co-ord_x6, co-ord_y6),   <-- hole (if present)
	#                                 (co-ord_x7, co-ord_y7),
	#                                 (co-ord_x8, co-ord_y8)] ],
	#               'type': 'Polygon'},
	#  'id': '1',
	#  'properties': OrderedDict([(u'NAME', u'Wales'), (u'LABEL', u'Wales')]),
	#  'type': 'Feature'}
	# 
	# Structure of a multipolygon geometry type
	# -----------------------------------------
	# In this case, multiple polygons are defined within each feature (rather then having
	# separate polygons defined as separate features as above).
	# Each feature will be represented as follows:
	#                                                                   POLYGON 1 WITH HOLE
	# {'geometry': {'coordinates': [ [ [(co-ord_x01, co-ord_y01),   <-- Linear ring
	#                                   (co-ord_x02, co-ord_y02),
	#                                   (co-ord_x03, co-ord_y03),
	#                                   (co-ord_x04, co-ord_y04),
	#                                   (co-ord_x05, co-ord_y05)]
	#
	#                                  [(co-ord_x06, co-ord_y06),   <-- hole (if present)
	#                                   (co-ord_x07, co-ord_y07),
	#                                   (co-ord_x08, co-ord_y08)] ]
	#                                                                   POLYGON 2 WITH HOLE
	#                                [ [(co-ord_x09, co-ord_y09),   <-- Linear ring
	#                                   (co-ord_x10, co-ord_y10),
	#                                   (co-ord_x11, co-ord_y11),
	#                                   (co-ord_x12, co-ord_y12),
	#                                   (co-ord_x13, co-ord_y13)]
	#
	#                                  [(co-ord_x14, co-ord_y14),   <-- hole (if present)
	#                                   (co-ord_x15, co-ord_y15),
	#                                   (co-ord_x16, co-ord_y16)] ] ],
	#               'type': 'MultiPolygon'},
	#  'id': '1',
	#  'properties': OrderedDict([(u'NAME', u'Scotland'), (u'LABEL', u'Scotland')]),
	#  'type': 'Feature'}
	#
	# To use phjReadPolygonPoints() function, pass the following variables:
	#     i. phjPolygonToRead = a tuple of tuples of coordinates (see above).
	#    ii. phjColumnNames = tuple of names of columns to be used in the dataframe.
	#   iii. phjFeatureNumber = integer representing the count of features read so far.
	#    iv. phjFeatureID = integer taken from feature['id'].
	#     v. phjFeatureName = string taken from feature['properties']['name'].
	#    vi. phjFeatureLabel = string taken from feature['properties']['label'].
	#   vii. phjGeomTypeName = string taken from feature['geometry']['type'] and is either
	#                          'Polygon' or 'MultiPolygon'.
	#  viii. phjMultipolgonNumber = integer representing the number of multipolygons read
	#                               or, in the case of polygon geometry type, equals 0.
	
	# Step through each polygon to read (LinearRing and holes)...
	phjPolygonNumber = 0	# Counter for the number of the polygon in the coordinates list
	# Define a dataframe that will temporarily store the points of the LinearRing and all holes
	phjTempFeatureDF = pd.DataFrame(columns=phjColumnNames)
	for phjPolygonCoords in phjPolygonToRead:
		# Set up a temporary dataframe to store the data for each polygon
		phjTempPolygonDF = pd.DataFrame(columns=phjColumnNames)
		# Create some vectors of repeated data to add to dataframe...
		phjTempLengthPolygon = len(phjPolygonCoords)
		print "Name:", phjFeatureName, "MultiPoly number:", phjMultiPolygonNumber, "Poly number:", phjPolygonNumber, "Number of vertices = ", phjTempLengthPolygon
		phjTempPolygonDF['feature_number']      = [phjFeatureNumber] * phjTempLengthPolygon
		phjTempPolygonDF['feature_id']          = [phjFeatureID] * phjTempLengthPolygon
		phjTempPolygonDF['name']                = [phjFeatureName] * phjTempLengthPolygon
		phjTempPolygonDF['label']               = [phjFeatureLabel] * phjTempLengthPolygon
		phjTempPolygonDF['geom_type']           = [phjGeomTypeName] * phjTempLengthPolygon
		phjTempPolygonDF['multipolygon_number'] = [phjMultiPolygonNumber] * phjTempLengthPolygon
		phjTempPolygonDF['polygon_number']      = [phjPolygonNumber] * phjTempLengthPolygon
		phjTempPolygonDF['point_number']        = range(phjTempLengthPolygon)
		phjTempPolygonDF['point']               = phjPolygonCoords
		#
		# Add the phjTempPolygonDF to the phjTempFeatureDF...
		phjTempFeatureDF = pd.concat([phjTempFeatureDF,phjTempPolygonDF], axis=0, ignore_index=True)
		# Increase polygon number counter
		phjPolygonNumber = phjPolygonNumber + 1
	
	return phjTempFeatureDF


def phjCalculatePolygonArea(phjDF,
							phjShpNumberName,
							phjVertex1XCoordinateName,
							phjVertex1YCoordinateName,
							phjVertex2XCoordinateName,
							phjVertex2YCoordinateName ):
	# See http://www.mathopenref.com/coordpolygonarea2.html for algorithm and explanation.
	# Bascially, the algorithm calculates the area between the edge and the y axis
	# Edges going "down" are positive (since x1-x2 is positive) whilst edges going
	# "up" are negative. Hence the sum of these edge areas will be the area of the
	# polygon - positive for clockwise polygons and negative for anticlockwise polygons.
	# In shapefiles, the direction in which polygons are labelled is important.
	# "Walking" around the polygon in a clockwise direction, the land to the
	# right is land within the polygon and land to the left is outside that polygon.
	# "Walking" around the polygon in an anti-clockwise direction, land to the right
	# is "land" whilst the area to the left is not land (it may, for example, be a lake).
	# Consequently, in shapefiles, the main LinearRing is labelled in a clockwise
	# direction whilst internal lakes are labelled in an anticlockwise direction.
	#
	# This algorithm is actually calculating the "signed" area of a 
	# polygon. If the area is positive, the polygon is clockwise; if negative, the
	# polygon is anticlockwise.
	# This is described briefly in an answer by Beta at:
	# http://stackoverflow.com/questions/1165647/how-to-determine-if-a-list-of-polygon-points-are-in-clockwise-order
	# (N.B. The actual answer given by Beta calculates the sum of the areas between
	# each edge and the x axis rather the y axis as used in the function.)
	
	phjArea = np.zeros(len(phjDF))
	
	phjAreaCounter = 0
	
	# Divide dataframe into groups based on shape number variable.
	for i in pd.unique(phjDF[phjShpNumberName]):
		print 'Shape number: ', i
		phjGroupDF = phjDF.ix[phjDF[phjShpNumberName]==i,[phjShpNumberName,phjVertex1XCoordinateName,phjVertex1YCoordinateName,phjVertex2XCoordinateName,phjVertex2YCoordinateName]]
		print phjGroupDF
		phjGroupLength = len(phjGroupDF)
		
		# Calculate the "edge area" (i.e. the area between the edge and the y axis) for
		# each edge. The "down" edges are positive and the "up" edges are negative.
		phjGroupDF['area'] = ( ((phjGroupDF[phjVertex1XCoordinateName] + phjGroupDF[phjVertex2XCoordinateName]) / 2) * (phjGroupDF[phjVertex1YCoordinateName] - phjGroupDF[phjVertex2YCoordinateName]) )
		
		# The signed area of the polygon is the sum of the "edge areas". Clockwise
		# polygons are positive and anticlockwise polygons are negative. Hence, the
		# area of the polygon is the absolute value of the signed area. The direction
		# of the polygon is given by the sign (positive = clockwise;
		# negative = anticlockwise).
		phjArea[phjAreaCounter:phjAreaCounter + phjGroupLength] = phjGroupDF['area'].sum()
		
		phjAreaCounter = phjAreaCounter + phjGroupLength
		
	if(phjAreaCounter != len(phjDF)):
		raise phjPolygonAreaError, "Final area counter was incorrect."
		
	# The phjArea array now contains the signed areas of each each polygon. If the sign
	# is '+' then the polygon is clockwise; if '-ve', the polygon is anticlockwise.
	# This function returns two arrays: the first is an array of the absolute areas, the
	# second is an array of bits where 1 = clockwise and 0 = anticlockwise.	
	
	return (np.absolute(phjArea), np.inverse(np.signbit(phjArea)).astype(int))


