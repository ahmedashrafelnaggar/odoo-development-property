
import xmlrpc.client

url = 'http://localhost:8069'

db = 'Hospital'

username = 'admin'

password = 'admin'


common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
# this is for authentication:
uid = common.authenticate(db, username, password, {})

if uid:
 print("Authenticatation successful")


 # this for read and search from database here to know how much company in model res_partner
 models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))


 # res.partner this model which you do that in this examples , you can do that on any model in the world (read ,search,search_count, create,write, also when you want to change status beta3et any model


 # search method:
 # partners = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['is_company', '=', True]]])
 partners = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['email', '=', 'www.ahmedashraf83@gmail.com']]])
 # partners = models.execute_kw(db, uid, password, 'hospital.patient', 'search', [[['email', '=', 'www.ahmedashraf83@gmail.com']]])
 print('partners is:', partners)

 #  search _count bethseb kam addad comapany add in model res.partner if find company this mean company =true
 partners_count = models.execute_kw(db, uid, password, 'res.partner', 'search_count', [[['is_company', '=', True]]])
 # partners_count = models.execute_kw(db, uid, password, 'hospital.patient', 'search_count', [[['is_company', '=', True]]])
 print("Partners_count is:", partners_count)
 # i ask it how much phone= '01122702847' in model res.partner, it appear Partners is: [1] this mean id = 1
 # limit is mean 5 numbers only for id but you have id = 1 only , one company only
 # partners = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['phone', '=', '01122702847']]])




 # res.partner this model which you do that in this examples , you can do that on any model in the world (read ,search,search_count, create,write, also when you want to change status beta3et any model

 # read method
 # [partners] we can put id number instead of partners like [10] this mean model elly id = 10 read id and namr neta3hom
 partner_rec=  models.execute_kw(db, uid, password, 'res.partner', 'read', [partners], {'fields': ['id', 'name']})
 # partner_rec=  models.execute_kw(db, uid, password, 'hospital.patient', 'read', [partners], {'fields': ['id', 'name']})
 print("Partner_rec is:", partner_rec)

 # search read
 # partner_rec2 = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['is_company', '=', True]]],{'fields': ['id', 'name'], 'limit': 5})
 # print("Partner_rec2 is:", partner_rec2)

 # create record in model res.partner
 # vals = {
 #  'name': "Odoo Mates External API ",
 #  'email': "odoomates@gmail.com ",
 # }
 # created_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [vals])
 # print("Created_id is:", created_id)



 # res.partner this model which you do that in this examples , you can do that on any model in the world (read ,search,search_count, create,write, also when you want to change status beta3et any model

 # write/update method
 # make this el model el  id = 10  or partners do update to phone and mobil this numbers
 # models.execute_kw(db, uid, password, 'res.partner', 'write', [[id], {'name': "Newer partner"}]) this is ka3eda
 models.execute_kw(db, uid, password, 'res.partner', 'write', [[10], {'phone': "01122702847", 'mobile': '5555', 'website':'WOW'}])
 # models.execute_kw(db, uid, password, 'hospital.patient', 'write', [[10], {'phone': "01122702847", 'mobile': '5555', 'website':'WOW'}])
 # models.execute_kw(db, uid, password, 'res.partner', 'write', [partners, {'phone': "01122702847", 'mobile': '5555', 'website':'WOW'}])

 # delete method
 # models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[id]]) this is ka3eda
 # this delete model which containe on id = 21
 # models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[23]])
 # models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[partners]])

 # method to make  state from draft to done through api , you told him make this model which contain id = 1 make state = done
 # models.execute_kw(db, uid, password, 'hospital.appointment', 'name_method _state',[id]) this is ka3eda
 # models.execute_kw(db, uid, password, 'hospital.appointment', 'action_done', [4])
 models.execute_kw(db, uid, password, 'hospital.appointment', 'action_in_consultation', [3])

else:
 print("Authenticatation failed")