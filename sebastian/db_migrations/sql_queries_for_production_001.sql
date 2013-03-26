

update portdata set country='United States' where id >181;
update portdata set region='North America' where id >181;
update portdata set country='Côte d''Ivoire' where id=4;
update portdata set country='Libya' where id=8;
update portdata set country='Libya' where id=9;
update portdata set country='North Korea' where id=39;
update portdata set country='Burma' where id=57;
update portdata set country='South Korea' where id=61;
update portdata set country='South Korea' where id=62;
update portdata set country='South Korea' where id=64;
update portdata set country='Taiwan' where id=66;
update portdata set country='Taiwan' where id=67;
update portdata set country='Vietnam' where id=69;
update portdata set country='Vietnam' where id=70;
update portdata set country='Russia' where id=86;
update portdata set country='Russia' where id=87;
update portdata set country='Venezuela' where id=177;


DROP TABLE IF EXISTS `citations`;

CREATE TABLE `citations` (
  `ID` int(11) NOT NULL,
  `name` tinytext NOT NULL,
  `source` mediumtext NOT NULL COMMENT 'Where it''s from. Aside from just being important to track where we get info, this would let us compare sources.  ',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


insert into citations (ID, name, source) Values (0, 'None', 'No known source');
insert into citations (ID, name, source) Values (1, 'WPI', 'World Port Index');

alter table portdata change column `reef-protected_area_present` reef_protected_area_present tinyint(1) not null default -1;

alter table portdata change column `sub-region` sub_region tinytext NOT NULL;

alter table portdata add column classification_cit_id INT NOT NULL DEFAULT 0 after classification;
alter table portdata add column existing_structure_cit_id INT NOT NULL DEFAULT 0 after existing_structure;
alter table portdata add column maintained_channel_depth_cit_id INT NOT NULL DEFAULT 0 after maintained_channel_depth;
alter table portdata add column maintained_channel_width_cit_id INT NOT NULL DEFAULT 0 after maintained_channel_width;
alter table portdata add column avg_channel_dredging_cit_id INT NOT NULL DEFAULT 0 after avg_channel_dredging;
alter table portdata add column infrastructure_area_cit_id INT NOT NULL DEFAULT 0 after infrastructure_area;
alter table portdata add column basin_area_cit_id INT NOT NULL DEFAULT 0 after basin_area;
alter table portdata add column measured_avg_defense_elevation_cit_id INT NOT NULL DEFAULT 0 after measured_avg_defense_elevation;
alter table portdata add column calculated_avg_defense_elevation_cit_id INT NOT NULL DEFAULT 0 after calculated_avg_defense_elevation;
alter table portdata add column measured_max_defense_elevation_cit_id INT NOT NULL DEFAULT 0 after measured_max_defense_elevation;
alter table portdata add column calculated_max_defense_elevation_cit_id INT NOT NULL DEFAULT 0 after calculated_max_defense_elevation;
alter table portdata add column measured_defense_length_cit_id INT NOT NULL DEFAULT 0 after measured_defense_length;
alter table portdata add column calculated_defense_length_cit_id INT NOT NULL DEFAULT 0 after calculated_defense_length;
alter table portdata add column population_density_cit_id INT NOT NULL DEFAULT 0 after population_density;
alter table portdata add column population_cit_id INT NOT NULL DEFAULT 0 after population;
alter table portdata add column bridge_present_cit_id INT NOT NULL DEFAULT 0 after bridge_present;
alter table portdata add column river_present_cit_id INT NOT NULL DEFAULT 0 after river_present;
alter table portdata add column river_names_cit_id INT NOT NULL DEFAULT 0 after river_names;
alter table portdata add column reef_protected_area_present INT NOT NULL DEFAULT 0 after reef_protected_area_present;
alter table portdata add column biologically_significant_environment_present_cit_id INT NOT NULL DEFAULT 0 after biologically_significant_environment_present;
alter table portdata add column subaquatic_geology_cit_id INT NOT NULL DEFAULT 0 after subaquatic_geology;

alter table portdata add column sediment_load_cit_id INT NOT NULL DEFAULT 0 after sediment_load;
alter table portdata add column watershed_area_cit_id INT NOT NULL DEFAULT 0 after watershed_area;
alter table portdata add column avg_river_discharge_cit_id INT NOT NULL DEFAULT 0 after avg_river_discharge;
alter table portdata add column peak_river_discharge_cit_id INT NOT NULL DEFAULT 0 after peak_river_discharge;
alter table portdata add column mean_low_low_tide_cit_id INT NOT NULL DEFAULT 0 after mean_low_low_tide;
alter table portdata add column mean_high_high_tide_cit_id INT NOT NULL DEFAULT 0 after mean_high_high_tide;
alter table portdata add column storm_surge_cit_id INT NOT NULL DEFAULT 0 after storm_surge;
alter table portdata add column design_wave_height_cit_id INT NOT NULL DEFAULT 0 after design_wave_height;
alter table portdata add column design_wave_period_cit_id INT NOT NULL DEFAULT 0 after design_wave_period;
alter table portdata add column sea_storm_return_period_cit_id INT NOT NULL DEFAULT 0 after sea_storm_return_period;
alter table portdata add column sea_storm_surge_wave_height_cit_id INT NOT NULL DEFAULT 0 after sea_storm_surge_wave_height;
alter table portdata add column river_storm_return_period_cit_id INT NOT NULL DEFAULT 0 after river_storm_return_period;
alter table portdata add column river_storm_design_flow_cit_id INT NOT NULL DEFAULT 0 after river_storm_design_flow;
alter table portdata add column metric_tonnage_cit_id INT NOT NULL DEFAULT 0 after metric_tonnage;
alter table portdata add column freight_tonnage_cit_id INT NOT NULL DEFAULT 0 after freight_tonnage;
alter table portdata add column revenue_tonnage_cit_id INT NOT NULL DEFAULT 0 after revenue_tonnage;
alter table portdata add column TEUs_cit_id INT NOT NULL DEFAULT 0 after TEUs;
alter table portdata add column shipping_export_value_cit_id INT NOT NULL DEFAULT 0 after shipping_export_value;
alter table portdata add column shipping_import_value_cit_id INT NOT NULL DEFAULT 0 after shipping_import_value;
alter table portdata add column shipping_total_value_cit_id INT NOT NULL DEFAULT 0 after shipping_total_value;
alter table portdata add column grid_height_cit_id INT NOT NULL DEFAULT 0 after grid_height;
alter table portdata add column grid_width_cit_id INT NOT NULL DEFAULT 0 after grid_width;
alter table portdata add column elev_data_cit_id INT NOT NULL DEFAULT 0 after elev_data;
alter table portdata add column shipping_volume_cit_id INT NOT NULL DEFAULT 0 after shipping_volume;



alter table conversions add column cit_id  INT NOT NULL DEFAULT 0 after source;



alter table data_request add column cit_id  INT NOT NULL DEFAULT 0 after complete;



alter table countries add column gravel_cit_id INT NOT NULL DEFAULT 0 after gravel;
alter table countries add column cement_cit_id INT NOT NULL DEFAULT 0 after cement;
alter table countries add column sand_cit_id INT NOT NULL DEFAULT 0 after sand;
alter table countries add column pop_density_cit_id INT NOT NULL DEFAULT 0 after pop_density;
alter table countries add column coastal_engineers_cit_id INT NOT NULL DEFAULT 0 after coastal_engineers;
alter table countries add column specialty_ships_cit_id INT NOT NULL DEFAULT 0 after specialty_ships;
alter table countries add column tugs_cit_id INT NOT NULL DEFAULT 0 after tugs;



alter table regions add column concrete_production_cit_id INT NOT NULL DEFAULT 0 after concrete_production;
alter table regions add column coastal_engineers_cit_id INT NOT NULL DEFAULT 0 after coastal_engineers;
alter table regions add column specialty_ships_cit_id INT NOT NULL DEFAULT 0 after specialty_ships;
alter table regions add column tug_boats_cit_id INT NOT NULL DEFAULT 0 after tug_boats;


alter table modelparameters add column eqn_cit_id INT NOT NULL DEFAULT 0 after eqn;
alter table modelparameters add column sea_level_rise_cit_id INT NOT NULL DEFAULT 0 after sea_level_rise;
alter table modelparameters add column freeboard_cit_id INT NOT NULL DEFAULT 0 after freeboard;
alter table modelparameters add column design_wave_height_cit_id INT NOT NULL DEFAULT 0 after design_wave_height;
alter table modelparameters add column storm_surge_cit_id INT NOT NULL DEFAULT 0 after storm_surge;
alter table modelparameters add column mean_high_high_tide_cit_id INT NOT NULL DEFAULT 0 after mean_high_high_tide;
alter table modelparameters add column mean_low_low_tide_cit_id INT NOT NULL DEFAULT 0 after mean_low_low_tide;
alter table modelparameters add column dike_flat_top_cit_id INT NOT NULL DEFAULT 0 after dike_flat_top;
alter table modelparameters add column foundation_height_cit_id INT NOT NULL DEFAULT 0 after foundation_height;
alter table modelparameters add column toe_height_cit_id INT NOT NULL DEFAULT 0 after toe_height;
alter table modelparameters add column outer_toe_slope_cit_id INT NOT NULL DEFAULT 0 after outer_toe_slope;
alter table modelparameters add column inner_toe_slope_cit_id INT NOT NULL DEFAULT 0 after inner_toe_slope;
alter table modelparameters add column outer_core_slope_cit_id INT NOT NULL DEFAULT 0 after outer_core_slope;
alter table modelparameters add column inner_core_slope_cit_id INT NOT NULL DEFAULT 0 after inner_core_slope;
alter table modelparameters add column core_flat_top_cit_id INT NOT NULL DEFAULT 0 after core_flat_top;
alter table modelparameters add column core_height_cit_id INT NOT NULL DEFAULT 0 after core_height;
alter table modelparameters add column outer_dike_slope_cit_id INT NOT NULL DEFAULT 0 after outer_dike_slope;
alter table modelparameters add column inner_dike_slope_cit_id INT NOT NULL DEFAULT 0 after inner_dike_slope;
alter table modelparameters add column armor_depth_cit_id INT NOT NULL DEFAULT 0 after armor_depth;
alter table modelparameters add column max_elevation_cit_id INT NOT NULL DEFAULT 0 after max_elevation;
alter table modelparameters add column min_elevation_cit_id INT NOT NULL DEFAULT 0 after min_elevation;

create database uws_maps;
grant all privileges on uws_maps.* to 'uws_maps'@'localhost' identified by 'littlemermaid';
grant all privileges on uws_maps.* to 'uws_ge'@'localhost' identified by 'littlemermaid';

DROP TABLE IF EXISTS `elev_data_africa_default_30sec`;
CREATE TABLE `elev_data_africa_default_30sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_asia_default_30sec`;
CREATE TABLE `elev_data_asia_default_30sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_europe_default_30sec`;
CREATE TABLE `elev_data_europe_default_30sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_middle_east_default_30sec`;
CREATE TABLE `elev_data_middle_east_default_30sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_north_america_default_30sec`;
CREATE TABLE `elev_data_north_america_default_30sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_oceania_default_30sec`;
CREATE TABLE `elev_data_oceania_default_30sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_south_america_default_30sec`;
CREATE TABLE `elev_data_south_america_default_30sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_africa_google_web_service`;
CREATE TABLE `elev_data_africa_google_web_service` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_asia_google_web_service`;
CREATE TABLE `elev_data_asia_google_web_service` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_europe_google_web_service`;
CREATE TABLE `elev_data_europe_google_web_service` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;







DROP TABLE IF EXISTS `elev_data_middle_east_google_web_service`;
CREATE TABLE `elev_data_middle_east_google_web_service` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_north_america_google_web_service`;
CREATE TABLE `elev_data_north_america_google_web_service` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_oceania_google_web_service`;
CREATE TABLE `elev_data_oceania_google_web_service` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_south_america_google_web_service`;
CREATE TABLE `elev_data_south_america_google_web_service` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_africa_usgs_3sec`;
CREATE TABLE `elev_data_africa_usgs_3sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_asia_usgs_3sec`;
CREATE TABLE `elev_data_asia_usgs_3sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_europe_usgs_3sec`;
CREATE TABLE `elev_data_europe_usgs_3sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_middle_east_usgs_3sec`;
CREATE TABLE `elev_data_middle_east_usgs_3sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_north_america_usgs_3sec`;
CREATE TABLE `elev_data_north_america_usgs_3sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_oceania_usgs_3sec`;
CREATE TABLE `elev_data_oceania_usgs_3sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_south_america_usgs_3sec`;
CREATE TABLE `elev_data_south_america_usgs_3sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;





DROP TABLE IF EXISTS `elev_data_all_default_30sec`;
CREATE TABLE `elev_data_all_default_30sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_all_google_web_service`;
CREATE TABLE `elev_data_all_google_web_service` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_all_usgs_3sec
`;
CREATE TABLE `elev_data_all_usgs_3sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;



insert into uws_maps.elev_data_africa_default_30sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_ge.archive_elev_data where (latitude>=-40 and latitude<=40) and ((longitude>=-20 and longitude<=60) or (false)) and source = 'default_30sec');
insert into uws_maps.elev_data_africa_google_web_service (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_ge.archive_elev_data where (latitude>=-40 and latitude<=40) and ((longitude>=-20 and longitude<=60) or (false)) and source = 'google_web_service');
insert into uws_maps.elev_data_africa_usgs_3sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_ge.archive_elev_data where (latitude>=-40 and latitude<=40) and ((longitude>=-20 and longitude<=60) or (false)) and source = 'usgs_3sec');
insert into uws_maps.elev_data_asia_default_30sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_ge.archive_elev_data where (latitude>=0 and latitude<=78) and ((longitude>=30 and longitude<=180) or (longitude>=-180 and longitude<=-169)) and source = 'default_30sec');
insert into uws_maps.elev_data_asia_google_web_service (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_ge.archive_elev_data where (latitude>=0 and latitude<=78) and ((longitude>=30 and longitude<=180) or (longitude>=-180 and longitude<=-169)) and source = 'google_web_service');
insert into uws_maps.elev_data_asia_usgs_3sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_ge.archive_elev_data where (latitude>=0 and latitude<=78) and ((longitude>=30 and longitude<=180) or (longitude>=-180 and longitude<=-169)) and source = 'usgs_3sec');
insert into uws_maps.elev_data_europe_default_30sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_ge.archive_elev_data where (latitude>=34 and latitude<=75) and ((longitude>=-25 and longitude<=60) or (false)) and source = 'default_30sec');
insert into uws_maps.elev_data_europe_google_web_service (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_ge.archive_elev_data where (latitude>=34 and latitude<=75) and ((longitude>=-25 and longitude<=60) or (false)) and source = 'google_web_service');
insert into uws_maps.elev_data_europe_usgs_3sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_ge.archive_elev_data where (latitude>=34 and latitude<=75) and ((longitude>=-25 and longitude<=60) or (false)) and source = 'usgs_3sec');
insert into uws_maps.elev_data_middle_east_default_30sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_ge.archive_elev_data where (latitude>=11 and latitude<=43) and ((longitude>=25 and longitude<=70) or (false)) and source = 'default_30sec');
insert into uws_maps.elev_data_middle_east_google_web_service (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_ge.archive_elev_data where (latitude>=11 and latitude<=43) and ((longitude>=25 and longitude<=70) or (false)) and source = 'google_web_service');
insert into uws_maps.elev_data_middle_east_usgs_3sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_ge.archive_elev_data where (latitude>=11 and latitude<=43) and ((longitude>=25 and longitude<=70) or (false)) and source = 'usgs_3sec');

insert into uws_maps.elev_data_north_america_default_30sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_ge.archive_elev_data where (latitude>=9 and latitude<=85) and ((longitude>=-173 and longitude<=-10) or (false)) and source = 'default_30sec');
insert into uws_maps.elev_data_north_america_google_web_service (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_ge.archive_elev_data where (latitude>=9 and latitude<=85) and ((longitude>=-173 and longitude<=-10) or (false)) and source = 'google_web_service');
insert into uws_maps.elev_data_north_america_usgs_3sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_ge.archive_elev_data where (latitude>=9 and latitude<=85) and ((longitude>=-173 and longitude<=-10) or (false)) and source = 'usgs_3sec');
insert into uws_maps.elev_data_oceania_default_30sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_ge.archive_elev_data where (latitude>=-53 and latitude<=21) and ((longitude>=90 and longitude<=180) or (longitude>=-180 and longitude<=-105)) and source = 'default_30sec');
insert into uws_maps.elev_data_oceania_google_web_service (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_ge.archive_elev_data where (latitude>=-53 and latitude<=21) and ((longitude>=90 and longitude<=180) or (longitude>=-180 and longitude<=-105)) and source = 'google_web_service');
insert into uws_maps.elev_data_oceania_usgs_3sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_ge.archive_elev_data where (latitude>=-53 and latitude<=21) and ((longitude>=90 and longitude<=180) or (longitude>=-180 and longitude<=-105)) and source = 'usgs_3sec');
insert into uws_maps.elev_data_south_america_default_30sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_ge.archive_elev_data where (latitude>=-57 and latitude<=23) and ((longitude>=-92 and longitude<=-31) or (false)) and source = 'default_30sec');
insert into uws_maps.elev_data_south_america_google_web_service (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_ge.archive_elev_data where (latitude>=-57 and latitude<=23) and ((longitude>=-92 and longitude<=-31) or (false)) and source = 'google_web_service');
insert into uws_maps.elev_data_south_america_usgs_3sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_ge.archive_elev_data where (latitude>=-57 and latitude<=23) and ((longitude>=-92 and longitude<=-31) or (false)) and source = 'usgs_3sec');

insert into uws_maps.elev_data_all_usgs_3sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_ge.archive_elev_data where source = 'usgs_3sec');
insert into uws_maps.elev_data_all_default_30sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_ge.archive_elev_data where source = 'default_30sec');
insert into uws_maps.elev_data_all_google_web_service (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_ge.archive_elev_data where source = 'google_web_service');



alter table portdata add column map_region TINYTEXT NOT NULL DEFAULT '' after region;
update portdata set map_region=ucase(replace(region,' ',''));


update portdata set region='North America' where region='';


DROP TABLE IF EXISTS `port_group`;

CREATE TABLE `port_group` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `name` tinytext NOT NULL,
  `primary_port_id` int(11) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


insert into port_group (primary_port_id) (select distinct(portid) from portprotector order by id);

update port_group pg, portdata pd set pg.name=pd.name where pd.id=pg.primary_port_id;

alter table portdata add column port_group INT NOT NULL after id;

update portdata pd, port_group pg set pd.port_group = pg.id where pd.id=pg.primary_port_id;

update portdata pd, port_group pg set pd.port_group = pg.id where pd.id=33 and pg.primary_port_id=28;
update portdata pd, port_group pg set pd.port_group = pg.id where pd.id=50 and pg.primary_port_id=52;
update portdata pd, port_group pg set pd.port_group = pg.id where pd.id=47 and pg.primary_port_id=54;
update portdata pd, port_group pg set pd.port_group = pg.id where pd.id=53 and pg.primary_port_id=54;
update portdata pd, port_group pg set pd.port_group = pg.id where pd.id=56 and pg.primary_port_id=60;
update portdata pd, port_group pg set pd.port_group = pg.id where pd.id=261 and pg.primary_port_id=118;
update portdata pd, port_group pg set pd.port_group = pg.id where pd.id=256 and pg.primary_port_id=142;
update portdata pd, port_group pg set pd.port_group = pg.id where (pd.id=249 or pd.id=250 or pd.id=251 or pd.id=252 )  and pg.primary_port_id=130;
update portdata pd, port_group pg set pd.port_group = pg.id where (pd.id=131 or pd.id=192 or pd.id=193 ) and pg.primary_port_id=136;
update portdata pd, port_group pg set pd.port_group = pg.id where (pd.id=140 or pd.id=200 or pd.id=201 or pd.id=202 or pd.id=203 or pd.id=204 or pd.id=205 )  and pg.primary_port_id=139;
update portdata pd, port_group pg set pd.port_group = pg.id where pd.id=126 and pg.primary_port_id=125;

insert into port_group (primary_port_id) (select id from portdata where port_group = '');
update port_group pg, portdata pd set pg.name=pd.name where pd.id=pg.primary_port_id;
update portdata pd, port_group pg set pd.port_group = pg.id where pd.id=pg.primary_port_id;


DROP TABLE IF EXISTS `elev_data_shard01_default_30sec`;
CREATE TABLE `elev_data_shard01_default_30sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard02_default_30sec`;
CREATE TABLE `elev_data_shard02_default_30sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard03_default_30sec`;
CREATE TABLE `elev_data_shard03_default_30sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard04_default_30sec`;
CREATE TABLE `elev_data_shard04_default_30sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard05_default_30sec`;
CREATE TABLE `elev_data_shard05_default_30sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard06_default_30sec`;
CREATE TABLE `elev_data_shard06_default_30sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard01_google_web_service`;
CREATE TABLE `elev_data_shard01_google_web_service` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard02_google_web_service`;
CREATE TABLE `elev_data_shard02_google_web_service` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard03_google_web_service`;
CREATE TABLE `elev_data_shard03_google_web_service` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;






DROP TABLE IF EXISTS `elev_data_shard04_google_web_service`;
CREATE TABLE `elev_data_shard04_google_web_service` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard05_google_web_service`;
CREATE TABLE `elev_data_shard05_google_web_service` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard06_google_web_service`;
CREATE TABLE `elev_data_shard06_google_web_service` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard01_usgs_3sec`;
CREATE TABLE `elev_data_shard01_usgs_3sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard02_usgs_3sec`;
CREATE TABLE `elev_data_shard02_usgs_3sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard03_usgs_3sec`;
CREATE TABLE `elev_data_shard03_usgs_3sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard04_usgs_3sec`;
CREATE TABLE `elev_data_shard04_usgs_3sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard05_usgs_3sec`;
CREATE TABLE `elev_data_shard05_usgs_3sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard06_usgs_3sec`;
CREATE TABLE `elev_data_shard06_usgs_3sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


insert into uws_maps.elev_data_shard01_default_30sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_all_default_30sec where ((longitude>=-180 and longitude<=-119) or (longitude>=179 and longitude<=180)) and source = 'default_30sec');
insert into uws_maps.elev_data_shard01_google_web_service (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_all_google_web_service where ((longitude>=-180 and longitude<=-119) or (longitude>=179 and longitude<=180)) and source = 'google_web_service');
insert into uws_maps.elev_data_shard01_usgs_3sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_all_usgs_3sec where ((longitude>=-180 and longitude<=-119) or (longitude>=179 and longitude<=180)) and source = 'usgs_3sec');
insert into uws_maps.elev_data_shard02_default_30sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_all_default_30sec where ((longitude>=-121 and longitude<=-59) or (false)) and source = 'default_30sec');
insert into uws_maps.elev_data_shard02_google_web_service (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_all_google_web_service where ((longitude>=-121 and longitude<=-59) or (false)) and source = 'google_web_service');
insert into uws_maps.elev_data_shard02_usgs_3sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_all_usgs_3sec where ((longitude>=-121 and longitude<=-59) or (false)) and source = 'usgs_3sec');
insert into uws_maps.elev_data_shard03_default_30sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_all_default_30sec where ((longitude>=-61 and longitude<=1) or (false)) and source = 'default_30sec');
insert into uws_maps.elev_data_shard03_google_web_service (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_all_google_web_service where ((longitude>=-61 and longitude<=1) or (false)) and source = 'google_web_service');
insert into uws_maps.elev_data_shard03_usgs_3sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_all_usgs_3sec where ((longitude>=-61 and longitude<=1) or (false)) and source = 'usgs_3sec');
insert into uws_maps.elev_data_shard04_default_30sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_all_default_30sec where ((longitude>=-1 and longitude<=61) or (false)) and source = 'default_30sec');
insert into uws_maps.elev_data_shard04_google_web_service (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_all_google_web_service where ((longitude>=-1 and longitude<=61) or (false)) and source = 'google_web_service');
insert into uws_maps.elev_data_shard04_usgs_3sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_all_usgs_3sec where ((longitude>=-1 and longitude<=61) or (false)) and source = 'usgs_3sec');


insert into uws_maps.elev_data_shard05_default_30sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_all_default_30sec where ((longitude>=59 and longitude<=121) or (false)) and source = 'default_30sec');
insert into uws_maps.elev_data_shard05_google_web_service (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_all_google_web_service where ((longitude>=59 and longitude<=121) or (false)) and source = 'google_web_service');
insert into uws_maps.elev_data_shard05_usgs_3sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_all_usgs_3sec where ((longitude>=59 and longitude<=121) or (false)) and source = 'usgs_3sec');
insert into uws_maps.elev_data_shard06_default_30sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_all_default_30sec where ((longitude>=119 and longitude<=180) or (longitude>=-180 and longitude<=-179)) and source = 'default_30sec');
insert into uws_maps.elev_data_shard06_google_web_service (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_all_google_web_service where ((longitude>=119 and longitude<=180) or (longitude>=-180 and longitude<=-179)) and source = 'google_web_service');
insert into uws_maps.elev_data_shard06_usgs_3sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_all_usgs_3sec where ((longitude>=119 and longitude<=180) or (longitude>=-180 and longitude<=-179)) and source = 'usgs_3sec');



create database uws_collect;
grant all privileges on uws_collect.* to 'uws_maps'@'localhost' identified by 'littlemermaid';
grant all privileges on uws_collect.* to 'uws_ge'@'localhost' identified by 'littlemermaid';
use uws_collect;


DROP TABLE IF EXISTS `setup_gather_google_web_service_3sec`;
CREATE TABLE `setup_gather_google_web_service_3sec` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `port_id` int(11) NOT NULL,
  `process_order` smallint NOT NULL,
  `current_run_id` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `last_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard01_google_web_service_3sec`;
CREATE TABLE `elev_data_shard01_google_web_service_3sec` (
  `run_id` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `collected` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `port_id` int(11) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `resolution` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard02_google_web_service_3sec`;
CREATE TABLE `elev_data_shard02_google_web_service_3sec` (
  `run_id` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `collected` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `port_id` int(11) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `resolution` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard03_google_web_service_3sec`;
CREATE TABLE `elev_data_shard03_google_web_service_3sec` (
  `run_id` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `collected` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `port_id` int(11) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `resolution` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard04_google_web_service_3sec`;
CREATE TABLE `elev_data_shard04_google_web_service_3sec` (
  `run_id` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `collected` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `port_id` int(11) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `resolution` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard05_google_web_service_3sec`;
CREATE TABLE `elev_data_shard05_google_web_service_3sec` (
  `run_id` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `collected` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `port_id` int(11) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `resolution` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard06_google_web_service_3sec`;
CREATE TABLE `elev_data_shard06_google_web_service_3sec` (
  `run_id` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `collected` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `port_id` int(11) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `resolution` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


insert into uws_collect.setup_gather_google_web_service_3sec (port_id,process_order,status) (select primary_port_id, primary_port_id, 'empty' from uws_ge.port_group order by primary_port_id);

use uws_maps;

DROP TABLE IF EXISTS `elev_data_shard01_google_web_service_3sec`;
CREATE TABLE `elev_data_shard01_google_web_service_3sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard02_google_web_service_3sec`;
CREATE TABLE `elev_data_shard02_google_web_service_3sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard03_google_web_service_3sec`;
CREATE TABLE `elev_data_shard03_google_web_service_3sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard04_google_web_service_3sec`;
CREATE TABLE `elev_data_shard04_google_web_service_3sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard05_google_web_service_3sec`;
CREATE TABLE `elev_data_shard05_google_web_service_3sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard06_google_web_service_3sec`;
CREATE TABLE `elev_data_shard06_google_web_service_3sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


use uws_collect;

DROP TABLE IF EXISTS `setup_gather_google_web_service_30sec`;
CREATE TABLE `setup_gather_google_web_service_30sec` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `port_id` int(11) NOT NULL,
  `process_order` smallint NOT NULL,
  `current_run_id` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `last_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard01_google_web_service_30sec`;
CREATE TABLE `elev_data_shard01_google_web_service_30sec` (
  `run_id` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `collected` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `port_id` int(11) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `resolution` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard02_google_web_service_30sec`;
CREATE TABLE `elev_data_shard02_google_web_service_30sec` (
  `run_id` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `collected` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `port_id` int(11) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `resolution` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard03_google_web_service_30sec`;
CREATE TABLE `elev_data_shard03_google_web_service_30sec` (
  `run_id` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `collected` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `port_id` int(11) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `resolution` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard04_google_web_service_30sec`;
CREATE TABLE `elev_data_shard04_google_web_service_30sec` (
  `run_id` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `collected` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `port_id` int(11) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `resolution` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard05_google_web_service_30sec`;
CREATE TABLE `elev_data_shard05_google_web_service_30sec` (
  `run_id` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `collected` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `port_id` int(11) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `resolution` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard06_google_web_service_30sec`;
CREATE TABLE `elev_data_shard06_google_web_service_30sec` (
  `run_id` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `collected` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `port_id` int(11) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `resolution` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


insert into uws_collect.setup_gather_google_web_service_30sec (port_id,process_order,status) (select primary_port_id, primary_port_id, 'empty' from uws_ge.port_group order by primary_port_id);

use uws_maps;

DROP TABLE IF EXISTS `elev_data_shard01_google_web_service_30sec`;
CREATE TABLE `elev_data_shard01_google_web_service_30sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard02_google_web_service_30sec`;
CREATE TABLE `elev_data_shard02_google_web_service_30sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard03_google_web_service_30sec`;
CREATE TABLE `elev_data_shard03_google_web_service_30sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard04_google_web_service_30sec`;
CREATE TABLE `elev_data_shard04_google_web_service_30sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard05_google_web_service_30sec`;
CREATE TABLE `elev_data_shard05_google_web_service_30sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard06_google_web_service_30sec`;
CREATE TABLE `elev_data_shard06_google_web_service_30sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


use uws_collect;

DROP TABLE IF EXISTS `setup_gather_google_web_service_point3sec`;
CREATE TABLE `setup_gather_google_web_service_point3sec` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `port_id` int(11) NOT NULL,
  `process_order` smallint NOT NULL,
  `current_run_id` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `last_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard01_google_web_service_point3sec`;
CREATE TABLE `elev_data_shard01_google_web_service_point3sec` (
  `run_id` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `collected` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `port_id` int(11) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `resolution` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard02_google_web_service_point3sec`;
CREATE TABLE `elev_data_shard02_google_web_service_point3sec` (
  `run_id` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `collected` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `port_id` int(11) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `resolution` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard03_google_web_service_point3sec`;
CREATE TABLE `elev_data_shard03_google_web_service_point3sec` (
  `run_id` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `collected` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `port_id` int(11) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `resolution` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard04_google_web_service_point3sec`;
CREATE TABLE `elev_data_shard04_google_web_service_point3sec` (
  `run_id` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `collected` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `port_id` int(11) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `resolution` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard05_google_web_service_point3sec`;
CREATE TABLE `elev_data_shard05_google_web_service_point3sec` (
  `run_id` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `collected` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `port_id` int(11) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `resolution` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard06_google_web_service_point3sec`;
CREATE TABLE `elev_data_shard06_google_web_service_point3sec` (
  `run_id` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `collected` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `port_id` int(11) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `resolution` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


insert into uws_collect.setup_gather_google_web_service_point3sec (port_id,process_order,status) (select primary_port_id, primary_port_id, 'empty' from uws_ge.port_group order by primary_port_id);

use uws_maps;

DROP TABLE IF EXISTS `elev_data_shard01_google_web_service_point3sec`;
CREATE TABLE `elev_data_shard01_google_web_service_point3sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard02_google_web_service_point3sec`;
CREATE TABLE `elev_data_shard02_google_web_service_point3sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard03_google_web_service_point3sec`;
CREATE TABLE `elev_data_shard03_google_web_service_point3sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard04_google_web_service_point3sec`;
CREATE TABLE `elev_data_shard04_google_web_service_point3sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard05_google_web_service_point3sec`;
CREATE TABLE `elev_data_shard05_google_web_service_point3sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard06_google_web_service_point3sec`;
CREATE TABLE `elev_data_shard06_google_web_service_point3sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


/* match up portprotector_history with portprotector */
alter table portprotector_history add column armor_volume DOUBLE NOT NULL after path_volume;
alter table portprotector_history add column foundation_volume DOUBLE NOT NULL after path_volume;
alter table portprotector_history add column toe_volume DOUBLE NOT NULL after path_volume;
alter table portprotector_history add column core_volume DOUBLE NOT NULL after path_volume;
alter table portprotector_history add column dike_volume  DOUBLE NOT NULL after path_volume;

/* add new values to portprotector_history and portprotector */
alter table portprotector add column riprap_volume DOUBLE NOT NULL after armor_volume;
alter table portprotector add column aggregate_volume DOUBLE NOT NULL after armor_volume;
alter table portprotector add column rebar_volume DOUBLE NOT NULL after armor_volume;
alter table portprotector add column cement_volume DOUBLE NOT NULL after armor_volume;

alter table portprotector add column riprap_weight DOUBLE NOT NULL after riprap_volume;
alter table portprotector add column aggregate_weight DOUBLE NOT NULL after riprap_volume;
alter table portprotector add column rebar_weight DOUBLE NOT NULL after riprap_volume;
alter table portprotector add column cement_weight DOUBLE NOT NULL after riprap_volume;

alter table portprotector_history add column riprap_volume DOUBLE NOT NULL after armor_volume;
alter table portprotector_history add column aggregate_volume DOUBLE NOT NULL after armor_volume;
alter table portprotector_history add column rebar_volume DOUBLE NOT NULL after armor_volume;
alter table portprotector_history add column cement_volume DOUBLE NOT NULL after armor_volume;

alter table portprotector_history add column riprap_weight DOUBLE NOT NULL after riprap_volume;
alter table portprotector_history add column aggregate_weight DOUBLE NOT NULL after riprap_volume;
alter table portprotector_history add column rebar_weight DOUBLE NOT NULL after riprap_volume;
alter table portprotector_history add column cement_weight DOUBLE NOT NULL after riprap_volume;



--
-- Table structure for table `berm_model`
--

DROP TABLE IF EXISTS `berm_model`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `berm_model` (
  `ID` mediumint(9) NOT NULL AUTO_INCREMENT,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `portID` mediumint(9) NOT NULL,
  `attribution` tinytext NOT NULL,
  `equation` tinytext NOT NULL,
  `elev_data` tinytext NOT NULL,
  `avg_elev` double NOT NULL,
  `path_length` double NOT NULL,
  `path_volume` double NOT NULL,
  `dike_volume` double NOT NULL,
  `core_volume` double NOT NULL,
  `toe_volume` double NOT NULL,
  `foundation_volume` double NOT NULL,
  `armor_volume` double NOT NULL,
  `cement_volume` double NOT NULL,
  `rebar_volume` double NOT NULL,
  `aggregate_volume` double NOT NULL,
  `riprap_volume` double NOT NULL,
  `cement_weight` double NOT NULL,
  `rebar_weight` double NOT NULL,
  `aggregate_weight` double NOT NULL,
  `riprap_weight` double NOT NULL,
  `path_geometry` geometry NOT NULL,
  `3Dfile` mediumtext NOT NULL,
  `computeCenter` tinytext NOT NULL,
  `grid_height` float NOT NULL,
  `grid_width` float NOT NULL,
  PRIMARY KEY (`ID`),
  SPATIAL KEY `PathGeom` (`path_geometry`),
  KEY `portID` (`portID`)
) ENGINE=MyISAM AUTO_INCREMENT=4325 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `berm_model_history`
--

DROP TABLE IF EXISTS `berm_model_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `berm_model_history` (
  `ID` mediumint(9) NOT NULL AUTO_INCREMENT,
  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `portID` mediumint(9) NOT NULL,
  `attribution` tinytext NOT NULL,
  `equation` tinytext NOT NULL,
  `elev_data` tinytext NOT NULL,
  `avg_elev` double NOT NULL,
  `path_length` double NOT NULL,
  `path_volume` double NOT NULL,
  `dike_volume` double NOT NULL,
  `core_volume` double NOT NULL,
  `toe_volume` double NOT NULL,
  `foundation_volume` double NOT NULL,
  `armor_volume` double NOT NULL,
  `cement_volume` double NOT NULL,
  `rebar_volume` double NOT NULL,
  `aggregate_volume` double NOT NULL,
  `riprap_volume` double NOT NULL,
  `cement_weight` double NOT NULL,
  `rebar_weight` double NOT NULL,
  `aggregate_weight` double NOT NULL,
  `riprap_weight` double NOT NULL,
  `path_geometry` geometry NOT NULL,
  `3Dfile` mediumtext NOT NULL,
  `computeCenter` tinytext NOT NULL,
  `grid_height` float NOT NULL,
  `grid_width` float NOT NULL,
  PRIMARY KEY (`ID`),
  SPATIAL KEY `PathGeom` (`path_geometry`),
  KEY `portID` (`portID`)
) ENGINE=MyISAM AUTO_INCREMENT=4195 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


/* add noaa/aster data tables */
use uws_maps;

DROP TABLE IF EXISTS `elev_data_all_noaa_aster_30m`;
CREATE TABLE `elev_data_all_noaa_aster_30m` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard01_noaa_aster_30m`;
CREATE TABLE `elev_data_shard01_noaa_aster_30m` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard02_noaa_aster_30m`;
CREATE TABLE `elev_data_shard02_noaa_aster_30m` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard03_noaa_aster_30m`;
CREATE TABLE `elev_data_shard03_noaa_aster_30m` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard04_noaa_aster_30m`;
CREATE TABLE `elev_data_shard04_noaa_aster_30m` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard05_noaa_aster_30m`;
CREATE TABLE `elev_data_shard05_noaa_aster_30m` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `elev_data_shard06_noaa_aster_30m`;
CREATE TABLE `elev_data_shard06_noaa_aster_30m` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/* shift loaded data from all to shard tables for noaa/aster */

insert into uws_maps.elev_data_shard01_noaa_aster_30m (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_all_noaa_aster_30m where ((longitude>=-180 and longitude<=-119) or (longitude>=179 and longitude<=180)) and source = 'noaa_aster_30m');

insert into uws_maps.elev_data_shard02_noaa_aster_30m (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_all_noaa_aster_30m where ((longitude>=-121 and longitude<=-59) or (false)) and source = 'noaa_aster_30m');

insert into uws_maps.elev_data_shard03_noaa_aster_30m (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_all_noaa_aster_30m where ((longitude>=-61 and longitude<=1) or (false)) and source = 'noaa_aster_30m');

insert into uws_maps.elev_data_shard04_noaa_aster_30m (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_all_noaa_aster_30m where ((longitude>=-1 and longitude<=61) or (false)) and source = 'noaa_aster_30m');

insert into uws_maps.elev_data_shard05_noaa_aster_30m (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_all_noaa_aster_30m where ((longitude>=59 and longitude<=121) or (false)) and source = 'noaa_aster_30m');

insert into uws_maps.elev_data_shard06_noaa_aster_30m (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_all_noaa_aster_30m where ((longitude>=119 and longitude<=180) or (longitude>=-180 and longitude<=-179)) and source = 'noaa_aster_30m');

/*
insert into elev_data_shard02_noaa_aster_30m_temp (latitude, longitude, elevation, source) select latitude, longitude, elevation, source from elev_data_shard02_noaa_aster_30m where id in (select max(id) from elev_data_shard02_noaa_aster_30m group by latitude, longitude having count(latitude) > 1);
*/


/* add temp google data table for noaa_aster_001666sec*/
use uws_maps;

DROP TABLE IF EXISTS `elev_data_all_google_web_service_30sec`;
CREATE TABLE `elev_data_all_google_web_service_30sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/* add temp google data table for noaa_aster_0008333sec*/
use uws_maps;

DROP TABLE IF EXISTS `elev_data_all_google_web_service_point3sec`;
CREATE TABLE `elev_data_all_google_web_service_point3sec` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4))
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


insert into uws_maps.elev_data_shard02_google_web_service_30sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_all_google_web_service_30sec where ((longitude>=-121 and longitude<=-59) or (false)) and source = 'google_web_service_30sec');


insert into uws_maps.elev_data_shard02_google_web_service_point3sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_all_google_web_service_point3sec where ((longitude>=-121 and longitude<=-59) or (false)) and source = 'google_web_service_point3sec');


