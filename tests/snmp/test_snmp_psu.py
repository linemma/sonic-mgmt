import pytest
from ansible_host import AnsibleHost
from test_snmp import check_snmp_ready

PSU_STATUS_OK = 2

@pytest.fixture(scope="module", autouse=True)
def setup_check_snmp_ready(testbed, testbed_devices):
    check_snmp_ready(testbed, testbed_devices)

@pytest.mark.bsl
def test_snmp_numpsu(testbed_devices, creds, duthost):

    ans_host = testbed_devices['dut']
    lhost = testbed_devices['localhost']
    hostip = ans_host.host.options['inventory_manager'].get_host(ans_host.hostname).vars['ansible_host']

    snmp_facts = lhost.snmp_facts(host=hostip, version="v2c", community=creds["snmp_rocommunity"])['ansible_facts']
    res = duthost.shell("psuutil numpsus")
    assert int(res[u'rc']) == 0, "Failed to get number of PSUs"

    numpsus = int(res['stdout'])
    assert numpsus == len(snmp_facts['snmp_psu'])


@pytest.mark.bsl
def test_snmp_psu_status(testbed_devices, creds):

    ans_host = testbed_devices['dut']
    lhost = testbed_devices['localhost']
    hostip = ans_host.host.options['inventory_manager'].get_host(ans_host.hostname).vars['ansible_host']

    snmp_facts = lhost.snmp_facts(host=hostip, version="v2c", community=creds["snmp_rocommunity"])['ansible_facts']

    for k, v in snmp_facts['snmp_psu'].items():
        if int(v['operstatus']) != PSU_STATUS_OK:
            pytest.fail("PSU {} operstatus is not OK!".format(k))
