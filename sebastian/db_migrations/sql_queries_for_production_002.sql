
/* add new model parameters to work with the updated volume spreadsheet formula */

insert into modelparameters (eqn , eqn_cit_id , sea_level_rise , sea_level_rise_cit_id , freeboard , freeboard_cit_id , design_wave_height , design_wave_height_cit_id , storm_surge , storm_surge_cit_id , mean_high_high_tide , mean_high_high_tide_cit_id , mean_low_low_tide , mean_low_low_tide_cit_id , dike_flat_top , dike_flat_top_cit_id , foundation_height , foundation_height_cit_id , toe_height , toe_height_cit_id , outer_toe_slope , outer_toe_slope_cit_id , inner_toe_slope , inner_toe_slope_cit_id , outer_core_slope , outer_core_slope_cit_id , inner_core_slope , inner_core_slope_cit_id , core_flat_top , core_flat_top_cit_id , core_height , core_height_cit_id , outer_dike_slope , outer_dike_slope_cit_id , inner_dike_slope , inner_dike_slope_cit_id , armor_depth , armor_depth_cit_id , max_elevation , max_elevation_cit_id , min_elevation , min_elevation_cit_id, max_elevation_berm , max_elevation_berm_cit_id , min_elevation_berm , min_elevation_berm_cit_id) values ('KDBS' , 0 , 2 , 0 , 0.5 , 0 , 0.5 , 0 , 0.5 , 0 , 1.5 , 0 , -1.5 , 0 , 10 , 0 , 2 , 0 , 3 , 0 , 10 , 0 , 1 , 0 , 5 , 0 , 3 , 0 , 6 , 0 , 3 , 0 , 5 , 0 , 3 , 0 , 2 , 0 , 40 , 0 , -60 , 0, 40 , 0 , -60 , 0);

/* adding fields for bucketing */
alter table portprotector add column bucket_count_20 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector add column bucket_count_19 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector add column bucket_count_18 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector add column bucket_count_17 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector add column bucket_count_16 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector add column bucket_count_15 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector add column bucket_count_14 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector add column bucket_count_13 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector add column bucket_count_12 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector add column bucket_count_11 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector add column bucket_count_10 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector add column bucket_count_9 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector add column bucket_count_8 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector add column bucket_count_7 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector add column bucket_count_6 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector add column bucket_count_5 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector add column bucket_count_4 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector add column bucket_count_3 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector add column bucket_count_2 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector add column bucket_count_1 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector add column bucket_low DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector add column bucket_high DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector add column number_of_buckets DOUBLE NOT NULL DEFAULT 0 after armor_volume;

alter table portprotector_history add column bucket_count_20 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector_history add column bucket_count_19 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector_history add column bucket_count_18 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector_history add column bucket_count_17 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector_history add column bucket_count_16 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector_history add column bucket_count_15 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector_history add column bucket_count_14 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector_history add column bucket_count_13 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector_history add column bucket_count_12 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector_history add column bucket_count_11 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector_history add column bucket_count_10 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector_history add column bucket_count_9 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector_history add column bucket_count_8 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector_history add column bucket_count_7 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector_history add column bucket_count_6 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector_history add column bucket_count_5 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector_history add column bucket_count_4 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector_history add column bucket_count_3 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector_history add column bucket_count_2 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector_history add column bucket_count_1 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector_history add column bucket_low DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector_history add column bucket_high DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table portprotector_history add column number_of_buckets DOUBLE NOT NULL DEFAULT 0 after armor_volume;

alter table berm_model add column bucket_count_20 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model add column bucket_count_19 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model add column bucket_count_18 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model add column bucket_count_17 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model add column bucket_count_16 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model add column bucket_count_15 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model add column bucket_count_14 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model add column bucket_count_13 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model add column bucket_count_12 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model add column bucket_count_11 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model add column bucket_count_10 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model add column bucket_count_9 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model add column bucket_count_8 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model add column bucket_count_7 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model add column bucket_count_6 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model add column bucket_count_5 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model add column bucket_count_4 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model add column bucket_count_3 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model add column bucket_count_2 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model add column bucket_count_1 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model add column bucket_low DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model add column bucket_high DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model add column number_of_buckets DOUBLE NOT NULL DEFAULT 0 after armor_volume;

alter table berm_model_history add column bucket_count_20 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model_history add column bucket_count_19 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model_history add column bucket_count_18 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model_history add column bucket_count_17 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model_history add column bucket_count_16 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model_history add column bucket_count_15 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model_history add column bucket_count_14 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model_history add column bucket_count_13 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model_history add column bucket_count_12 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model_history add column bucket_count_11 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model_history add column bucket_count_10 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model_history add column bucket_count_9 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model_history add column bucket_count_8 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model_history add column bucket_count_7 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model_history add column bucket_count_6 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model_history add column bucket_count_5 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model_history add column bucket_count_4 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model_history add column bucket_count_3 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model_history add column bucket_count_2 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model_history add column bucket_count_1 DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model_history add column bucket_low DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model_history add column bucket_high DOUBLE NOT NULL DEFAULT 0 after armor_volume;
alter table berm_model_history add column number_of_buckets DOUBLE NOT NULL DEFAULT 0 after armor_volume;


/* removing fields for bucketing */
/*
alter table portprotector drop column bucket_count_12;
alter table portprotector drop column bucket_count_11;
alter table portprotector drop column bucket_count_10;
alter table portprotector drop column bucket_count_9;
alter table portprotector drop column bucket_count_8;
alter table portprotector drop column bucket_count_7;
alter table portprotector drop column bucket_count_6;
alter table portprotector drop column bucket_count_5;
alter table portprotector drop column bucket_count_4;
alter table portprotector drop column bucket_count_3;
alter table portprotector drop column bucket_count_2;
alter table portprotector drop column bucket_count_1;
alter table portprotector drop column number_of_buckets;

alter table portprotector_history drop column bucket_count_12;
alter table portprotector_history drop column bucket_count_11;
alter table portprotector_history drop column bucket_count_10;
alter table portprotector_history drop column bucket_count_9;
alter table portprotector_history drop column bucket_count_8;
alter table portprotector_history drop column bucket_count_7;
alter table portprotector_history drop column bucket_count_6;
alter table portprotector_history drop column bucket_count_5;
alter table portprotector_history drop column bucket_count_4;
alter table portprotector_history drop column bucket_count_3;
alter table portprotector_history drop column bucket_count_2;
alter table portprotector_history drop column bucket_count_1;
alter table portprotector_history drop column number_of_buckets;

alter table berm_model drop column bucket_count_12;
alter table berm_model drop column bucket_count_11;
alter table berm_model drop column bucket_count_10;
alter table berm_model drop column bucket_count_9;
alter table berm_model drop column bucket_count_8;
alter table berm_model drop column bucket_count_7;
alter table berm_model drop column bucket_count_6;
alter table berm_model drop column bucket_count_5;
alter table berm_model drop column bucket_count_4;
alter table berm_model drop column bucket_count_3;
alter table berm_model drop column bucket_count_2;
alter table berm_model drop column bucket_count_1;
alter table berm_model drop column number_of_buckets;

alter table berm_model_history drop column bucket_count_12;
alter table berm_model_history drop column bucket_count_11;
alter table berm_model_history drop column bucket_count_10;
alter table berm_model_history drop column bucket_count_9;
alter table berm_model_history drop column bucket_count_8;
alter table berm_model_history drop column bucket_count_7;
alter table berm_model_history drop column bucket_count_6;
alter table berm_model_history drop column bucket_count_5;
alter table berm_model_history drop column bucket_count_4;
alter table berm_model_history drop column bucket_count_3;
alter table berm_model_history drop column bucket_count_2;
alter table berm_model_history drop column bucket_count_1;
alter table berm_model_history drop column number_of_buckets;
*/


/* adding fields from new volume spreadsheet formula */
alter table portprotector add column structural_steel_volume DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table portprotector add column structural_steel_weight DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table portprotector add column concrete_volume DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table portprotector add column small_riprap_volume DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table portprotector add column large_riprap_volume DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table portprotector add column quarry_run_stone_volume DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table portprotector add column gravel_volume DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table portprotector add column sand_volume DOUBLE NOT NULL DEFAULT -1 after armor_volume;

alter table portprotector_history add column structural_steel_volume DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table portprotector_history add column structural_steel_weight DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table portprotector_history add column concrete_volume DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table portprotector_history add column small_riprap_volume DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table portprotector_history add column large_riprap_volume DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table portprotector_history add column quarry_run_stone_volume DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table portprotector_history add column gravel_volume DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table portprotector_history add column sand_volume DOUBLE NOT NULL DEFAULT -1 after armor_volume;

alter table berm_model add column structural_steel_volume DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table berm_model add column structural_steel_weight DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table berm_model add column concrete_volume DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table berm_model add column small_riprap_volume DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table berm_model add column large_riprap_volume DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table berm_model add column quarry_run_stone_volume DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table berm_model add column gravel_volume DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table berm_model add column sand_volume DOUBLE NOT NULL DEFAULT -1 after armor_volume;

alter table berm_model_history add column structural_steel_volume DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table berm_model_history add column structural_steel_weight DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table berm_model_history add column concrete_volume DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table berm_model_history add column small_riprap_volume DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table berm_model_history add column large_riprap_volume DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table berm_model_history add column quarry_run_stone_volume DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table berm_model_history add column gravel_volume DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table berm_model_history add column sand_volume DOUBLE NOT NULL DEFAULT -1 after armor_volume;

alter table portprotector add column structure_height_above_msl DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table portprotector_history add column structure_height_above_msl DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table berm_model add column structure_height_above_msl DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table berm_model_history add column structure_height_above_msl DOUBLE NOT NULL DEFAULT -1 after armor_volume;

alter table portprotector add column tallest_section_depth DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table portprotector_history add column tallest_section_depth DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table berm_model add column tallest_section_depth DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table berm_model_history add column tallest_section_depth DOUBLE NOT NULL DEFAULT -1 after armor_volume;

alter table portprotector add column shortest_section_depth DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table portprotector_history add column shortest_section_depth DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table berm_model add column shortest_section_depth DOUBLE NOT NULL DEFAULT -1 after armor_volume;
alter table berm_model_history add column shortest_section_depth DOUBLE NOT NULL DEFAULT -1 after armor_volume;



alter table portprotector drop column cement_volume;
alter table portprotector drop column rebar_volume;
alter table portprotector drop column aggregate_volume;
alter table portprotector drop column riprap_volume;
alter table portprotector drop column cement_weight;
alter table portprotector drop column rebar_weight;
alter table portprotector drop column aggregate_weight;
alter table portprotector drop column riprap_weight;

alter table portprotector_history drop column cement_volume;
alter table portprotector_history drop column rebar_volume;
alter table portprotector_history drop column aggregate_volume;
alter table portprotector_history drop column riprap_volume;
alter table portprotector_history drop column cement_weight;
alter table portprotector_history drop column rebar_weight;
alter table portprotector_history drop column aggregate_weight;
alter table portprotector_history drop column riprap_weight;

alter table berm_model drop column cement_volume;
alter table berm_model drop column rebar_volume;
alter table berm_model drop column aggregate_volume;
alter table berm_model drop column riprap_volume;
alter table berm_model drop column cement_weight;
alter table berm_model drop column rebar_weight;
alter table berm_model drop column aggregate_weight;
alter table berm_model drop column riprap_weight;

alter table berm_model_history drop column cement_volume;
alter table berm_model_history drop column rebar_volume;
alter table berm_model_history drop column aggregate_volume;
alter table berm_model_history drop column riprap_volume;
alter table berm_model_history drop column cement_weight;
alter table berm_model_history drop column rebar_weight;
alter table berm_model_history drop column aggregate_weight;
alter table berm_model_history drop column riprap_weight;


update portdata set grid_height=0.75, grid_width=0.95 where id=60;
update portdata set grid_height=0.5, grid_width=0.65 where id=61;
update portdata set grid_height=0.35, grid_width=0.75 where id=29;
update portdata set grid_height=0.85, grid_width=0.95 where id=50;
update portdata set grid_height=1.4, grid_width=1.8 where id=139;


update modelparameters set eqn='WBMAS' where id=2;
