
'''
License:
  "NASA Open Source Agreement 1.3"

Description:
  Build science products from Landsat L4TM, L5TM, and L7ETM+ data.

History:
  Original Development (cdr_ecv.py) by David V. Hill, USGS/EROS
  Created Jan/2014 by Ron Dilley, USGS/EROS
    - Gutted the original implementation from cdr_ecv.py and placed it in
      this file.
'''

# espa-common objects and methods
from espa_constants import *


class ErrorCodes:
    '''
    Description:
      Defines the error codes to use for cdr_ecv core processing.
    '''

    ##########################################################################
    # Use EXIT_SUCCESS for 0
    # Use EXIT_FAILURE for 1
    ##########################################################################

    # TODO - NOT GENERATED
    exception = 2  # Exited on an exception that does not have a specific code

    # Generated by processor.ProductProcessor.initialize_processing_directory
    creating_stage_dir = 3
    creating_work_dir = 4
    creating_output_dir = 5

    # Generated by processor.LandsatProcessor.stage_input_data
    # Generated by processor.ModisProcessor.stage_input_data
    # Generated by processor.PlotProcessor.stage_input_data
    staging_data = 6

    # Generated by processor.LandsatProcessor.stage_input_data
    # Generated by processor.ModisProcessor.stage_input_data
    unpacking = 7

    # Generated by processor.LandsatProcessor.stage_input_data
    metadata = 8

    # Generated by processor.LandsatProcessor.generate_sr_products
    surface_reflectance = 9

    # TODO - NOT GENERATED
    browse = 10

    # Generated by processor.LandsatProcessor.generate_spectral_indices
    spectral_indices = 11

    # TODO - NOT GENERATED
    create_dem = 12

    # TODO - NOT GENERATED
    solr = 13

    # Generated by processor.LandsatProcessor.generate_cfmask
    cfmask = 14

    # TODO - NOT GENERATED
    dswe = 15

    # Generated by processor.LandsatProcessor.cleanup_work_dir
    cleanup_work_dir = 16

    # Generated by warp.update_espa_xml
    # Generated by warp.warp_espa_data
    warping = 17

    # Generated by statistics.generate_statistics
    statistics = 18

    # Generated by distribution.tar_product
    # Generated by distribution.gzip_product
    # Generated by distribution.package_product
    # Generated by distribution.distribute_product
    # Generated by distribution.distribute_statistics
    # Generated by distribution.deliver_product
    packaging_product = 19

    # Generated by distribution.deliver_product
    # Generated by processor.LandsatProcessor.distribute_statistics
    distributing_product = 20

    # Generated by distribution.distribute_statistics
    # Generated by distribution.deliver_product
    verifing_checksum = 21

    # Generated by processor.CDRProcessor.remove_products_from_xml
    # Generated by processor.LandsatProcessor.cleanup_work_dir
    remove_products = 22

    # Generated by warp.reformat
    # Generated by processor.LandsatProcessor.convert_to_raw_binary
    # Generated by processor.ModisProcessor.convert_to_raw_binary
    reformat = 23

# END class ErrorCodes


class ESPAException(Exception):
    '''
    Description:
      Create a special ESPA exception for returning errors back up to the
      main or top-level calling routine.  This allows that routine to make
      decisions based on the error code and move on.
    '''

    # Define our error code attribute
    error_code = EXIT_SUCCESS

    def __init__(self, error_code, message):

        # Call the base class constructor
        Exception.__init__(self, message)

        # Set our error code
        self.error_code = error_code
# END class ESPAException
