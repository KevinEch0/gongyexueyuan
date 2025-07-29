-- 1. 插入顶级菜单（pid=0 指向自身）
INSERT INTO t_menu (id, name, level, path) VALUES (-1, '全部', 0, NULL);

-- 2. 插入一级菜单（pid=0）
INSERT INTO t_menu (id, name, level, pid) VALUES (1, '用户管理', 1, -1);
INSERT INTO t_menu (id, name, level, pid) VALUES (2, '权限管理', 1, -1);
INSERT INTO t_menu (id, name, level, pid) VALUES (3, '算法管理', 1, -1);
INSERT INTO t_menu (id, name, level, pid) VALUES (4, '数据管理', 1, -1);

-- 3. 插入二级菜单
INSERT INTO t_menu (id, name, level, path,pid) VALUES (11,'用户列表', 2,  '/user_list', 1);
INSERT INTO t_menu (id, name, level, path,pid) VALUES (21,'角色列表', 2, '/author_list', 2);
INSERT INTO t_menu (id, name, level, path,pid) VALUES (22,'权限列表', 2, '/role_list', 2);
INSERT INTO t_menu (id, name, level, path,pid) VALUES (31,'算法列表', 2, '/algorithm_list',3);
INSERT INTO t_menu (id, name, level, path,pid) VALUES (41,'数据分析与挖掘', 2,  '/data_analysis',4);
INSERT INTO t_menu (id, name, level, path,pid) VALUES (42,'数据可视化与报表', 2, '/data_visualization',4);

-- 4. 插入三级菜单
INSERT INTO t_menu (id, name, level, path,pid) VALUES (411,'实时数据分析', 3, '/data_analysis_realtime',41);
INSERT INTO t_menu (id, name, level, path,pid) VALUES (412,'历史数据分析', 3, '/data_analysis_history',41);
INSERT INTO t_menu (id, name, level, path,pid) VALUES (421,'可视化的界面', 3, '/data_visualization_interface',42);
INSERT INTO t_menu (id, name, level, path,pid) VALUES (422,'自定义报表', 3, '/data_visualization_report',42);
INSERT INTO t_menu (id, name, level, path,pid) VALUES (423,'多维度展示', 3,  '/data_visualization_dimension',42);