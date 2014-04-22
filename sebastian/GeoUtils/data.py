#!/usr/bin/python
# David Newell
# data/__init__.py
# Data module

# Form Dictionaries
# Format:
#    'Order. Fieldset Name' : { 'Field Name/ID' : ['type','label',[options],'DB field or value','hint'] }
# Note: options only required for checkbox, radio, select (drop-down), and multiple items
#
import constants
from database import RDB

# Returns a dict listing all countries. This is used to provide a dropdown menu in the
# port charactersitics.
def getCountries():
    DBhandle = RDB()
    DBhandle.connect('uws_ge')

    countries, count = DBhandle.query('SELECT name FROM countries')

    out = {}
    for elem in countries:
        out[elem['name']] = elem['name']

    DBhandle.close()
    return out


class FormDicts:
    PortChar = {
            'A. Port Details' : {
                    'PortID' : ['text','Port ID',['readonly'],'ID','You are not permitted to edit this item.'],
                    'PortName' : ['text','Port Name',[''],'name','Port name for research purposes <em>(may differ from common/local name)</em>'],
                    'AltName' : ['text','Alternate Name',[''],'alt_name','If there is a common or local name for this port that differs from the research name, please provide it here.'],
                    'Classification' : ['text','Classification',[''],'classification','Port setting classification. Future use may include automatic design models.'],
                    'ExistingDefense' : ['text','Existing Defense',[''],'existing_structure','Does a defensive structure already exist?']
                },
            'B. Geographic Information' : {
                    'Longitude' : ['text','Longitude',[''],'longitude','In decimal degrees (0.000000)'],
                    'Latitude' : ['text','Latitude',[''],'latitude','In decimal degrees (0.000000)'],
                    'Country' : ['select','Country', getCountries(),'country',''],
                    # I'm taking these out because region is determined by country - Ben P.
                    #'Region' : ['text','Region',[''],'region',''],
                    #'SubRegion' : ['text','Sub-region',[''],'sub_region','More local region'],
                    'WaterBody' : ['text','Body of Water',[''],'water_body','Nearest major body of water'],
                    'RiverNames' : ['textarea','River Name(s)',{'cols' : 30,'rows' : 2},'river_names','One per line']
                },
            'C. Channel Parameters' : {
                    'ChannelDepth' : ['text','Maintained Channel Depth',[''],'maintained_channel_depth','meters'],
                    'ChannelWidth' : ['text','Maintained Channel Width',[''],'maintained_channel_width','meters'],
                    'ChannelDredging' : ['text','Average Yearly Channel Dredging',[''],'avg_channel_dredging','meters/year']
                },
            'E. Defense Information' : {
                    'InfrastructureArea' : ['text','Infrastructure Area',['readonly'],'infrastructure_area','square meters'],
                    'BasinArea' : ['text','Basin Area',['readonly'],'basin_area','square meters'],
                    'MsrdAvgDefenseElevation' : ['text','Measured Avg Defense Elevation',[''],'measured_avg_defense_elevation','meters'],
                    'CalcAvgDefenseElevation' : ['text','Calculated Avg Defense Elevation',['readonly'],'calculated_avg_defense_elevation','meters'],
                    'MsrdMaxDefenseElevation' : ['text','Measured Max Defense Elevation',[''],'measured_max_defense_elevation','meters'],
                    'CalcMaxDefenseElevation' : ['text','Calculated Max Defense Elevation',['readonly'],'calculated_max_defense_elevation','meters'],
                    'MsrdDefenseLength' : ['text','Measured Defense Length',[''],'measured_defense_length',''],
                    'CalcDefenseLength' : ['text','Calculated Defense Length',['readonly'],'calculated_defense_length','']
                },
            'F. Population Data' : {
                    'PopulationDensity' : ['text','Population Density',[''],'population_density','per square kilometer'],
                    'TotalPopulation' : ['text','Total Population',[''],'population','thousands'],
                    'PopulationSource' : ['text','Population Source',[''],'population_data_source','What\s the source of these data?']
                },
            'G. Environmental Information' : {
                    'ReefProtectedArea' : ['radio','Reef/Protected Area Present',{'Yes' : 1,'No' : 0},'reef_protected_area_present',''],
                    'BioSignificantEnviron' : ['radio','Biologically Significant Environment Present',{'Yes' : 1,'No' : 0},'biologically_significant_environment_present',''],
                    'SubaquaticGeology' : ['text','Subaquatic Geology',[''],'subaquatic_geology',''],
                    'SedimentLoad' : ['text','Sediment Load',[''],'sediment_load','cubic meters/hour <em>(* tentative unit)</em>'],
                    'WatershedArea' : ['text','Watershed Area',[''],'watershed_area','square kilometers'],
                    'AvgRiverDischarge' : ['text','Average River Discharge',[''],'avg_river_discharge','cubic meters/second'],
                    'MaxRiverDischarge' : ['text','Maximum/Peak River Discharge',[''],'peak_river_discharge','cubic meters/second']
                },
            'H. Tidal Data' : {
                    'MeanLowTide' : ['text','Mean Low-Low Tide',[''],'mean_low_low_tide','meters above or below mean sea level'],
                    'MeanHighTide' : ['text','Mean High-High Tide Level',[''],'mean_high_high_tide','meters above or below mean sea level'],
                    'StormSurgeLevel' : ['text','Storm Surge Level',[''],'storm_surge','meters'],
                    'WaveHeight' : ['text','Design Wave Height',[''],'design_wave_height','meters'],
                    'WavePeriod' : ['text','Design Wave Period',[''],'design_wave_period','seconds']
                },
            'I. Storm Risk Parameters' : {
                    'SeaStormReturnPeriod' : ['text','Sea Storm Return Period',[''],'sea_storm_return_period','years'],
                    'SeaStormWaveHeight' : ['text','Sea Storm Surge Wave Height',[''],'sea_storm_surge_wave_height','meters'],
                    'RiverStormReturnPeriod' : ['text','River Storm Return Period',[''],'river_storm_return_period','years'],
                    'RiverStormDesignFlow' : ['text','River Storm Design Flow Rate',[''],'river_storm_design_flow','cubic meters/second']
                },
            'J. Shipping Information' : {
                    'MetricTonnage' : ['text','Metric Tonnage',[''],'metric_tonnage','metric tons'],
                    'FreightTonnage' : ['text','Freight Tonnage',[''],'freight_tonnage','freight tons'],
                    'RevenueTonnage' : ['text','Revenue Tonnage',[''],'revenue_tonnage','revenue tons'],
                    'TEUs' : ['text','Twenty-Foot Equivalent Units',[''],'TEUs','thousand TEUs'],
                    'ExportValue' : ['text','Export Value',[''],'shipping_export_value','current US dollars'],
                    'ImportValue' : ['text','Import Value',[''],'shipping_import_value','current US dollars'],
                    'TotalTradeValue' : ['text','Total Trade Value',[''],'shipping_total_value','current US dollars']
                },
            'K. Port Analysis Status' : {
                    'AnalysisComplete' : ['radio','What is the progress of analysis for this port?',{'Complete' : 2 , 'Partially Complete' : 1 , 'Incomplete' : 0},'analysis_complete','This value will alter the icon\'s color to indicate analysis progress.']
                },
            'zbuttons' : {
                    'Submit' : ['submit','Submit',[''],'','']
                },
            'zhidden' : {
                    'GE_KEY' : ['hidden','',[''],'GE_KEY',''],
                    'itemType' : ['hidden','',[''],'PortChar','']
                }
        }

    PortPoly = {
            'A. Port Polygon Details' : {
                    'ID' : ['text','Polygon ID',['readonly'],'ID','You are not permitted to edit this item.'],
                    #'PortID' : ['text','Port ID',[''],'portID','Use caution when editing this polygon\'s port association.'],
                    'PortID' : ['text','Port ID',['readonly'],'portID','You are not permitted to edit this item.'],
                    'PolyType' : ['select','Polygon Type',{'Port Infrastructure Polygon' : 'Port Infrastructure Polygon' , 'Basin Polygon' : 'Basin Polygon' , 'Model Avoid Polygon' : 'Model Avoid Polygon' ,'Model StartEnd Polygon' : 'Model StartEnd Polygon', 'Berm Avoid Polygon' : 'Berm Avoid Polygon'},'feature_type','Select the type of polygon'],
                    'newKML' : ['textarea','Paste new KML polygon here',{'cols' : 50,'rows' : 6},'feature_geometry','Draw a polygon using Google Earth\'s tools and copy, then paste, here. KML will be parsed automatically for coordinates.'],
                    'PolyArea' : ['text','Polygon Area',['readonly'],'feature_area','square meters. You are not permitted to edit this item.'],
                    'PolyPeri' : ['text','Polygon Perimeter',['readonly'],'feature_perimeter','meters. You are not permitted to edit this item.']
                },
            'zbuttons' : {
                    'Submit' : ['submit','Submit',[''],'','']
                },
            'zhidden' : {
                    'GE_KEY' : ['hidden','',[''],'GE_KEY',''],
                    'itemType' : ['hidden','',[''],'PortPoly','']
                }
        }

    PortProtectorModel = {
            'A. Port Protector Parameters' : {
                    'PortID' : ['text','Port ID',['readonly'],'ID','You are not permitted to edit this item.'],
                    'Equation' : ['select','Equation',
                                                {constants.Equations.KDBS : 'Version 2, SUPERSLR Minimum-Criteria Dike Design',
                                                 constants.Equations.BMASW : 'Ben and Merel\'s Attempt to Save the World',
                                                 constants.Equations.SMCDD : 'SUPERSLR Minimum-Criteria Dike Design'},
                                        'equation','Select the equation you wish to use for this model run.'],
                    'GridHeight' : ['text','Grid Height',[''],'height','degrees<br/>\nHeight of the elevation grid over which the model will run.'],
                    'GridWidth' : ['text','Grid Width',[''],'width','degrees<br/>\nWidth of the elevation grid over which the model will run.'],
                    'ElevationData' : ['select','Elevation Grid',{'default_30sec' : 'Default - UCSD - 30 arc-second' , 'usgs_3sec' : 'USGS - 3 arc-second' , 'google_web_service' : 'Google Elevation Data API' },'elev_data','Select the elevation grid you wish to use for this model run.']
                },
            'zbuttons' : {
                    'Submit' : ['submit','Run Model',[''],'','']
                },
            'zhidden' : {
                    'GE_KEY' : ['hidden','',[''],'GE_KEY',''],
                    'itemType' : ['hidden','',[''],'PortProtectorModel','']
                }
        }

    ModelPath = {
            'A. Model Result Details' : {
                    'AvgElev' : ['text','Average Elevation',['readonly'],'avg_elev','meters<br/>\nYou are not permitted to edit this item.'],
                    'PathLength' : ['text','Path Length',['readonly'],'path_length','meters<br/>\nYou are not permitted to edit this item.'],
                    'PathVolume' : ['text','Path Volume',['readonly'],'path_volume','cubic meters<br/>\nYou are not permitted to edit this item.'],
                    'DikeVolume' : ['text','Dike Volume',['readonly'],'dike_volume','cubic meters<br/>\nYou are not permitted to edit this item.'],
                    'CoreVolume' : ['text','Core Volume',['readonly'],'core_volume','cubic meters<br/>\nYou are not permitted to edit this item.'],
                    'ToeVolume' : ['text','Toe Volume',['readonly'],'toe_volume','cubic meters<br/>\nYou are not permitted to edit this item.'],
                    'FoundationVolume' : ['text','Foundation Volume',['readonly'],'foundation_volume','cubic meters<br/>\nYou are not permitted to edit this item.'],
                    'ArmorVolume' : ['text','Armor Volume',['readonly'],'armor_volume','cubic meters<br/>\nYou are not permitted to edit this item.']
                },
            'B. Model Run Details' : {
                    'ID' : ['text','Path ID',['readonly'],'ID','You are not permitted to edit this item.'],
                    'PortID' : ['text','Port ID',['readonly'],'portID','You are not permitted to edit this item.'],
                    'RequestedBy' : ['text','Requested by',['readonly'],'attribution','You are not permitted to edit this item.'],
                    'Timestamp' : ['text','Time of model run',['readonly'],'timestamp','Pacific Time<br/>\nYou are not permitted to edit this item.'],
                    'Equation' : ['text','Equation Used',['readonly'],'equation','You are not permitted to edit this item.'],
                    'ElevData' : ['text','Elevation Data',['readonly'],'elev_data','You are not permitted to edit this item.'],
                    'ComputeCenter' : ['text','Compute Center',['readonly'],'computeCenter','You are not permitted to edit this item.']
                },
            'zbuttons' : {
                    'Submit' : ['submit','Run Model',[''],'','']
                },
            'zhidden' : {
                    'GE_KEY' : ['hidden','',[''],'GE_KEY',''],
                    'itemType' : ['hidden','',[''],'ModelPath','']
                }
        }

    BermPath = {
            'A. Berm Result Details' : {
                    'AvgElev' : ['text','Average Elevation',['readonly'],'avg_elev','meters<br/>\nYou are not permitted to edit this item.'],
                    'PathLength' : ['text','Path Length',['readonly'],'path_length','meters<br/>\nYou are not permitted to edit this item.'],
                    'PathVolume' : ['text','Path Volume',['readonly'],'path_volume','cubic meters<br/>\nYou are not permitted to edit this item.'],
                    'DikeVolume' : ['text','Dike Volume',['readonly'],'dike_volume','cubic meters<br/>\nYou are not permitted to edit this item.'],
                    'CoreVolume' : ['text','Core Volume',['readonly'],'core_volume','cubic meters<br/>\nYou are not permitted to edit this item.'],
                    'ToeVolume' : ['text','Toe Volume',['readonly'],'toe_volume','cubic meters<br/>\nYou are not permitted to edit this item.'],
                    'FoundationVolume' : ['text','Foundation Volume',['readonly'],'foundation_volume','cubic meters<br/>\nYou are not permitted to edit this item.'],
                    'ArmorVolume' : ['text','Armor Volume',['readonly'],'armor_volume','cubic meters<br/>\nYou are not permitted to edit this item.']
                },
            'B. Berm Run Details' : {
                    'ID' : ['text','Path ID',['readonly'],'ID','You are not permitted to edit this item.'],
                    'PortID' : ['text','Port ID',['readonly'],'portID','You are not permitted to edit this item.'],
                    'RequestedBy' : ['text','Requested by',['readonly'],'attribution','You are not permitted to edit this item.'],
                    'Timestamp' : ['text','Time of model run',['readonly'],'timestamp','Pacific Time<br/>\nYou are not permitted to edit this item.'],
                    'Equation' : ['text','Equation Used',['readonly'],'equation','You are not permitted to edit this item.'],
                    'ElevData' : ['text','Elevation Data',['readonly'],'elev_data','You are not permitted to edit this item.'],
                    'ComputeCenter' : ['text','Compute Center',['readonly'],'computeCenter','You are not permitted to edit this item.']
                },
            'zbuttons' : {
                    'Submit' : ['submit','Run Berm',[''],'','']
                },
            'zhidden' : {
                    'GE_KEY' : ['hidden','',[''],'GE_KEY',''],
                    'itemType' : ['hidden','',[''],'BermPath','']
                }
        }


    Country = {
            'A. Country' : {
                    'Name' : ['text', 'Country Name', ['readonly'], 'name', 'You are not permitted to edit this item.'],
                    'Region' : ['text', 'Region Name', ['readonly'], 'sub_region', 'You are not permitted to edit this item.'],
                    'Parent Region' : ['text', 'Parent Region', ['readonly'], 'region', 'Your are not permitted to edit this item.'],
                    'ID' : ['text', 'ID', ['readonly'], 'ID', 'You are not permitted to edit this item.'],
                    'Population Density' : ['text', 'Population Density', [''], 'pop_density', 'People per km<sup>2</sup>']
                },
            'B. Resources' : {
                    'Concrete Production' : ['text', 'Cement Production', [''], 'cement', 'In thousand metric tons per year'],
                    'Gravel Production' : ['text', 'Gravel Production', [''], 'gravel', 'In thousand metric tons per year'],
                    'Sand Production' : ['text', 'Sand Production', [''], 'sand', 'In thousand metric tons per year'],
                    'Coastal Engineers' : ['text', 'Coastal Engineers', [''], 'coastal_engineers', 'Number in region'],
                    'Specialty Ships' : ['text', 'Specialty Ships', [''], 'specialty_ships', 'Number in region'],
                    'Tug Boats' : ['text', 'Tug Boats', [''], 'tugs', 'Number in region']
                },
            'zbuttons' : {
                    'Submit' : ['submit', 'Submit', [''],'','']
                },
            'zhidden' : {
                    'GE_KEY' : ['hidden', '', [''], 'GE_KEY', ''],
                    'itemType' : ['hidden', '', [''], 'Country', '']
                }
    }


    UserNote = {
            'A. User Note Details' : {
                    'ID' : ['text','ID',['readonly'],'ID','You are not permitted to edit this item.'],
                    'Author' : ['text','Author',['readonly'],'attribution','You are not permitted to edit this item.'],
                    'Timestamp' : ['text','Time of last update',['readonly'],'timestamp','Pacific Time<br/>\nYou are not permitted to edit this item.'],
                    'Show' : ['radio','Note Visible?',{'Yes' : 1 , 'No' : 0},'visible','If no, this note will not be accessible.'],
                    'Status' : ['select','Note Type',{'Caution' : 'Caution' , 'Sticky' : 'Sticky' , 'Info' : 'Info'},'status','Specifies icon style to display'],
                    'Details' : ['textarea','Note Contents',{'cols' : 50,'rows' : 6},'details','Details of note'],
                    'newKML' : ['textarea','Paste new KML point here',{'cols' : 50,'rows' : 6},'feature_geometry','Create a point using Google Earth\'s tools and copy, then paste, here. KML will be parsed automatically for coordinates.']

                },
            'zbuttons' : {
                    'Submit' : ['submit','Submit',[''],'','']
                },
            'zhidden' : {
                    'GE_KEY' : ['hidden','',[''],'GE_KEY',''],
                    'itemType' : ['hidden','',[''],'UserNote','']
                }
        }

    DataRequest = {
            'A. Data Request Details' : {
                    'ID' : ['text','ID',[],'ID','You are not permitted to edit this item.'],
                    'RequestType' : ['textarea','Note Contents',{'cols' : 50,'rows' : 6},'details','Details of note']
                },
            'zbuttons' : {
                    'Submit' : ['submit','Submit',[''],'','']
                },
            'zhidden' : {
                    'GE_KEY' : ['hidden','',[''],'GE_KEY',''],
                    'itemType' : ['hidden','',[''],'UserNote','']
                }
        }

    DeleteForm = {
            'A. Item Details' : {
                    'ID' : ['text','ID',['readonly'],'ID','You are not permitted to edit this item.'],
                    'AreYouSure' : ['radio','Are you sure?',{'Yes' : 1 , 'No' : 0},'areyousure','Are you really sure you want to delete this item? WARNING: Items are not recoverable once deleted.']
                },
            'zbuttons' : {
                    'Submit' : ['submit','Delete Item',[''],'','']
                },
            'zhidden' : {
                    'GE_KEY' : ['hidden','',[''],'GE_KEY',''],
                    'itemType' : ['hidden','',[''],'itemType','']
                }
        }


# Interface Dictionaries
# Format:
#    'Link Name' : [ icon, link , [ list of variable options ] , { dict of specified options } ]
# Note: options only required for checkbox, radio, select (drop-down), and multiple items
class InterfaceDicts:
    PortChar = {
            'View/Edit Port Data' : ['lens','/sebastian/interface/edit.py',['id','type','GE_KEY','edit'],{'' : ''}],
            'Add Port Polygon' : ['add','/sebastian/interface/create.py',['id','GE_KEY','edit'],{'type' : 'PortPoly'}],
            'Run Port Protector Model' : ['info','/sebastian/interface/model.py',['id','type','GE_KEY','edit'],{'' : ''}],
            'Add a Note' : ['add','/sebastian/interface/create.py',['id','GE_KEY','edit'],{'type' : 'UserNote'}]
        }

    PortPoly = {
            'Edit Port Polygon' : ['lens','/sebastian/interface/edit.py',['id','type','GE_KEY','edit'],{'' : ''}],
            'Delete Port Polygon' : ['delete','/sebastian/interface/delete.py',['id','type','GE_KEY','edit'],{'' : ''}],
            'Add a Note' : ['add','/sebastian/interface/create.py',['id','GE_KEY','edit'],{'type' : 'UserNote'}]
        }

    ModelPath = {
            'View Model Data' : ['lens','/sebastian/interface/edit.py',['id','type','GE_KEY'],{'edit' : '0'}],
            'Add Port Polygon' : ['add','/sebastian/interface/create.py',['id','GE_KEY','edit'],{'type' : 'PortPoly'}],
            'Add a Note' : ['add','/sebastian/interface/create.py',['id','GE_KEY','edit'],{'type' : 'UserNote'}]
        }

    BermPath = {
            'View Berm Data' : ['lens','/sebastian/interface/edit.py',['id','type','GE_KEY'],{'edit' : '0'}],
            'Add Port Polygon' : ['add','/sebastian/interface/create.py',['id','GE_KEY','edit'],{'type' : 'PortPoly'}],
            'Add a Note' : ['add','/sebastian/interface/create.py',['id','GE_KEY','edit'],{'type' : 'UserNote'}]
        }

    Country = {
                'View/Edit Country Info' : ['lens', '/sebastian/interface/edit.py', ['id', 'type', 'GE_KEY', 'edit'], {'' : ''}]
        }

    UserNote = {
            'Edit Note' : ['lens','/sebastian/interface/edit.py',['id','type','GE_KEY','edit'],{'' : ''}],
            'Add a Note' : ['add','/sebastian/interface/create.py',['id','GE_KEY','edit'],{'type' : 'UserNote'}]
        }

    Main = {
            'Let\'s see some information' : ['lens','/sebastian/interface/info/intro.py',[''],{}],
            'Add New Port' : ['add','/sebastian/interface/create.py',['id','GE_KEY','edit'],{'type' : 'PortChar'}],
            'Add a Note' : ['add','/sebastian/interface/create.py',['id','GE_KEY','edit'],{'type' : 'UserNote'}]
        }


