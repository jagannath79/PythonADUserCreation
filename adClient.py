import datetime
import requests
import rpyc


AD_SERVER_IP = '192.168.0.6'
AD_BOT_PORT = '19961'
domain_controller = 'DC=virtulux,DC=com'
users_ou = 'OU=ScriptTest,{}'.format(domain_controller)
groups_ou = 'OU=APAC,OU=SecurityGroups,{}'.format(domain_controller)
domain = '@virtulux.com'

def send_command(command):
    try:
        connection = rpyc.connect(AD_SERVER_IP, AD_BOT_PORT)
        connection.root.run_command(command)
    except Exception as Err:
        print('Error in send command', str(Err))

def create_user(username, givenname, sn, samaccount, office, title, department, company, manager, employee_id, display_name, active=False):
    """
        Create New user in AD
        :param username:
        :param employee_id:
        :param display_name:
        :param active:
        :return:
    """
    if active:
        disabled = 'no'
    else:
        disabled = 'yes'

    description = "User added by AD BOT on {}".format(datetime.datetime.now())
    default_password = 'DefaultP@55w0rD'
    un = givenname + "." + sn
    displayname = sn+"\, "+givenname
    displayname2 = sn+", "+givenname
    display_name = displayname2
    officeinfo = office
    titleinfo = title
    departmentinfo = department
    companyinfo = company
    managerinfo = manager


    dn = '"CN={},{}"'.format(displayname, users_ou)
    upn = '{}{}'.format(un, domain)

    groups = '"cn=NA-InfoSec-8-SOC-GA,{}" ' \
             '"cn=Global-InfoSec-8-SOC-GA,{}" '.format(groups_ou,
                                        groups_ou)
    command = 'dsadd user ' \
              '{} ' \
              '-fn "{}" '\
              '-ln "{}" ' \
              '-office "{}" ' \
              '-title "{}" ' \
              '-dept "{}" ' \
              '-company "{}" ' \
              '-mgr "{}" '\
              '-samid "{}" ' \
              '-upn "{}" ' \
              '-display "{}" ' \
              '-empid "{}" ' \
              '-desc "{}" ' \
              '-disabled {} ' \
              '-pwd {} ' \
              '-pwdneverexpires no ' \
              '-mustchpwd yes ' \
              '-memberof {} ' \
              '-acctexpires never ' \
              ''.format(
                         dn,
                         givenname,
                         sn,
                         officeinfo,
                         titleinfo,
                         departmentinfo,
                         companyinfo,
                         managerinfo,
                         samaccount,
                         upn,
                         display_name,
                         employee_id,
                         description,
                         disabled,
                         default_password,
                         groups,

                    )
    print(command)
    send_command(command)

create_user('Satavelekar, Krishan', 'Krishan', 'Satavelekar', 'insatk01','Virtlux India Hyderabad', 'Sr. Project Manager', 'Virtulux Security', 'Virtulux India', 'CN=Nambiar\, Gokul,OU=APAC IM Software,OU=ScriptTest,DC=virtulux,DC=com', '213002','Satavelekar, Krishan', active=True)