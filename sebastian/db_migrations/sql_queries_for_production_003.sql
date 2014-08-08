wget http://topex.ucsd.edu/cgi-bin/get_srtm30.cgi --post-data="north=60.5&south=60.4&west=70.4&east=70.5" -O"xyz1.txt"

use uws_maps;

DROP TABLE IF EXISTS `elev_data_upload`;
CREATE TABLE `elev_data_upload` (
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `elevation` double NOT NULL,
  `source` tinytext NOT NULL,
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `source` (`source`(4)),
  UNIQUE KEY `datapoint` (`latitude`,`longitude`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


load data infile 'data_upload.txt' REPLACE INTO TABLE elev_data_upload (longitude,latitude,elevation);

update elev_data_upload set source = 'default_30sec';

insert into uws_maps.elev_data_shard01_default_30sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_upload where ((longitude>=-180 and longitude<=-119) or (longitude>=179 and longitude<=180)) and source = 'default_30sec');
insert into uws_maps.elev_data_shard01_google_web_service (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_upload where ((longitude>=-180 and longitude<=-119) or (longitude>=179 and longitude<=180)) and source = 'google_web_service');
insert into uws_maps.elev_data_shard01_usgs_3sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_upload where ((longitude>=-180 and longitude<=-119) or (longitude>=179 and longitude<=180)) and source = 'usgs_3sec');
insert into uws_maps.elev_data_shard02_default_30sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_upload where ((longitude>=-121 and longitude<=-59) or (false)) and source = 'default_30sec');
insert into uws_maps.elev_data_shard02_google_web_service (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_upload where ((longitude>=-121 and longitude<=-59) or (false)) and source = 'google_web_service');
insert into uws_maps.elev_data_shard02_usgs_3sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_upload where ((longitude>=-121 and longitude<=-59) or (false)) and source = 'usgs_3sec');
insert into uws_maps.elev_data_shard03_default_30sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_upload where ((longitude>=-61 and longitude<=1) or (false)) and source = 'default_30sec');
insert into uws_maps.elev_data_shard03_google_web_service (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_upload where ((longitude>=-61 and longitude<=1) or (false)) and source = 'google_web_service');
insert into uws_maps.elev_data_shard03_usgs_3sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_upload where ((longitude>=-61 and longitude<=1) or (false)) and source = 'usgs_3sec');


insert into uws_maps.elev_data_shard04_default_30sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_upload where ((longitude>=-1 and longitude<=61) or (false)) and source = 'default_30sec');
insert into uws_maps.elev_data_shard04_google_web_service (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_upload where ((longitude>=-1 and longitude<=61) or (false)) and source = 'google_web_service');
insert into uws_maps.elev_data_shard04_usgs_3sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_upload where ((longitude>=-1 and longitude<=61) or (false)) and source = 'usgs_3sec');
insert into uws_maps.elev_data_shard05_default_30sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_upload where ((longitude>=59 and longitude<=121) or (false)) and source = 'default_30sec');
insert into uws_maps.elev_data_shard05_google_web_service (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_upload where ((longitude>=59 and longitude<=121) or (false)) and source = 'google_web_service');
insert into uws_maps.elev_data_shard05_usgs_3sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_upload where ((longitude>=59 and longitude<=121) or (false)) and source = 'usgs_3sec');
insert into uws_maps.elev_data_shard06_default_30sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_upload where ((longitude>=119 and longitude<=180) or (longitude>=-180 and longitude<=-179)) and source = 'default_30sec');
insert into uws_maps.elev_data_shard06_google_web_service (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_upload where ((longitude>=119 and longitude<=180) or (longitude>=-180 and longitude<=-179)) and source = 'google_web_service');
insert into uws_maps.elev_data_shard06_usgs_3sec (latitude,longitude,elevation,source) (select latitude,longitude,elevation,source from uws_maps.elev_data_upload where ((longitude>=119 and longitude<=180) or (longitude>=-180 and longitude<=-179)) and source = 'usgs_3sec');
