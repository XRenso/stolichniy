import pymongo


class Mongo:
    def __init__(self):
        self.connection = pymongo.MongoClient("mongodb://localhost:27017/")['stolichniy']
        self.user = self.connection['user']
        self.reff = self.connection['refferal']
        self.reff_settings = self.connection['refferal_settings']

    def create_user(self,fullname,user_id):
        if self.user.count_documents({'user_id':user_id})==0:

            user ={
                'user_id':user_id, #user_id пользователя
                'fullname':fullname, #полное имя пользователя
                'bonuses':0 #количество бонусов
            }
            self.user.insert_one(user)
            return 1
        return 0
    def get_user(self,user_id):
        return self.user.find_one({'user_id':user_id})

    def add_bonuses(self,user_id:str,bonuses:int):
        self.user.update_one({'user_id':user_id},{'$inc':{'bonuses':bonuses}})

    def create_refferal_setting(self,reff_code:str,name:str,desc:str,for_new_users:bool,per_user:bool,per_user_bonus:int,levels:dict):
        if self.reff_settings.count_documents({'code': reff_code}) == 0:

            refferal = {
                'code':reff_code, #уникальный код для реферальной программы
                'name':name,#Название рефералки
                'description':desc,#Описание рефералки
                'only_new_user':for_new_users, #Только ли для новых пользователей,
                'per_user':per_user, #Формат начисления бонусов, за каждого рефералла или по уровням
                'per_user_bonus':per_user_bonus,#Сколько начислять за 1 реферала
                'levels':levels #Уровни реферальных наград, если 2 предыдущих пунтка ложны
            }
            self.reff_settings.insert_one(refferal)
            return 1
        return 0

    def get_refferal_setting(self,reff_code:str):
        return self.reff_settings.find_one({'code':reff_code})


    def create_refferal(self,user_id,reff_code):
        if self.reff.count_documents({'reff_code':reff_code,'creator':user_id}) == 0:
            uniqie_code = self.get_last_refferal_code()
            refferal={
                'code':int(uniqie_code)+1 if uniqie_code else 1,
                'reff_code':reff_code,
                'creator':user_id,
                'activators':[]
            }
            print(refferal['code'])
            self.reff.insert_one(refferal)
            return refferal['code']

        return self.reff.find_one({'reff_code':reff_code,'creator':user_id})['code']


    def activate_refferal(self,reff_code,user_id):
        reff = self.get_refferal_by_code(reff_code)
        if user_id not in reff['activators']:
            self.reff.update_one({'code':reff_code},{"$push":{'activators':user_id}})
            return 1
        return 0
    def get_refferal_by_code(self, reff_code):
        return self.reff.find_one({'code': reff_code})

    def get_refferal_by_user_id(self,user_id,settings_code):
        return self.reff.find_one({'reff_code':settings_code,'creator':user_id})
    def get_last_refferal_code(self):
        try:
            return self.reff.find({}).sort({'_id': -1})[0]['code']
        except TypeError:
            return 1

    def get_all_user_refferals(self,user_id):
        return list(self.reff.find({'creator':user_id}))


if __name__ == '__main__':
    db = Mongo()
    # db.create_refferal_setting(
    #     reff_code='per_level',
    #     name='Проверка 1 за уровень',
    #     desc='Проверка система за каждого пользователя',
    #     for_new_users=True,
    #     per_user=True,
    #     per_user_bonus=10,
    #     levels={}
    #
    # )
    # db.create_refferal(483058216,'per_level')
    print(sorted([10,4,9,8]))
    # print('9'*64)