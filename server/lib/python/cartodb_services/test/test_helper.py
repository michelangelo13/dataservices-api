from datetime import datetime, date
from mock import Mock, MagicMock
import random
import sys
from mock_plpy import MockPlPy

plpy_mock = MockPlPy()
sys.modules['plpy'] = plpy_mock


def build_redis_user_config(redis_conn, username, quota=100, soft_limit=False,
                            service="heremaps", isolines_quota=0,
                            do_quota=None, soft_do_limit=None,
                            do_general_quota=None, soft_do_general_limit=None,
                            end_date=datetime.today()):
    user_redis_name = "rails:users:{0}".format(username)
    redis_conn.hset(user_redis_name, 'soft_geocoding_limit', soft_limit)
    redis_conn.hset(user_redis_name, 'geocoding_quota', quota)
    redis_conn.hset(user_redis_name, 'here_isolines_quota', isolines_quota)
    redis_conn.hset(user_redis_name, 'geocoder_provider', service)
    redis_conn.hset(user_redis_name, 'isolines_provider', service)
    redis_conn.hset(user_redis_name, 'routing_provider', service)
    redis_conn.hset(user_redis_name, 'period_end_date', end_date)
    if do_quota:
        redis_conn.hset(user_redis_name, 'obs_snapshot_quota', do_quota)
    if soft_do_limit:
        redis_conn.hset(user_redis_name, 'soft_obs_snapshot_limit',
                        soft_do_limit)
    if do_general_quota:
        redis_conn.hset(user_redis_name, 'obs_general_quota', do_general_quota)
    if soft_do_general_limit:
        redis_conn.hset(user_redis_name, 'soft_obs_general_limit',
                        soft_do_general_limit)
    redis_conn.hset(user_redis_name, 'google_maps_client_id', '')
    redis_conn.hset(user_redis_name, 'google_maps_api_key', '')


def build_redis_org_config(redis_conn, orgname, quota=100, service="heremaps",
                           isolines_quota=0, do_quota=None,
                           do_general_quota=None, end_date=datetime.today()):
    org_redis_name = "rails:orgs:{0}".format(orgname)
    redis_conn.hset(org_redis_name, 'geocoding_quota', quota)
    redis_conn.hset(org_redis_name, 'here_isolines_quota', isolines_quota)
    if do_quota:
        redis_conn.hset(org_redis_name, 'obs_snapshot_quota', do_quota)
    if do_general_quota:
        redis_conn.hset(org_redis_name, 'obs_snapshot_quota', do_quota)
    redis_conn.hset(org_redis_name, 'period_end_date', end_date)
    redis_conn.hset(org_redis_name, 'google_maps_client_id', '')
    redis_conn.hset(org_redis_name, 'google_maps_api_key', '')


def increment_service_uses(redis_conn, username, orgname=None,
                           date=date.today(), service='geocoder_here',
                           metric='success_responses', amount=20):
    prefix = 'org' if orgname else 'user'
    entity_name = orgname if orgname else username
    yearmonth = date.strftime('%Y%m')
    redis_name = "{0}:{1}:{2}:{3}:{4}".format(prefix, entity_name,
                                              service, metric, yearmonth)
    redis_conn.zincrby(redis_name, date.day, amount)


def plpy_mock_config():
    plpy_mock._define_result("CDB_Conf_GetConf\('heremaps_conf'\)", [{'conf': '{"geocoder": {"app_id": "app_id", "app_code": "code", "geocoder_cost_per_hit": 1}, "isolines": {"app_id": "app_id", "app_code": "code"}}'}])
    plpy_mock._define_result("CDB_Conf_GetConf\('mapzen_conf'\)", [{'conf': '{"routing": {"api_key": "api_key_rou", "monthly_quota": 1500000}, "geocoder": {"api_key": "api_key_geo", "monthly_quota": 1500000}, "matrix": {"api_key": "api_key_mat", "monthly_quota": 1500000}}'}])
    plpy_mock._define_result("CDB_Conf_GetConf\('logger_conf'\)", [{'conf': '{"geocoder_log_path": "/dev/null"}'}])
    plpy_mock._define_result("CDB_Conf_GetConf\('data_observatory_conf'\)", [{'conf': '{"connection": {"whitelist": ["ethervoid"], "production": "host=localhost port=5432 dbname=dataservices_db user=geocoder_api", "staging": "host=localhost port=5432 dbname=dataservices_db user=geocoder_api"}}'}])
    plpy_mock._define_result("CDB_Conf_GetConf\('server_conf'\)", [{'conf': '{"environment": "testing"}'}])
    plpy_mock._define_result("select txid_current", [{'txid': random.randint(0, 1000)}])
