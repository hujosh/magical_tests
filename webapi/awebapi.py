import aiohttp


class AHTTP:
    def __init__(self, user, domain = 'magic.al', site = 'dev'):
        self.user = user
        self.domain = domain
        self.site = site
        self.url = "https://%s.%s"%(self.site, self.domain)
        self._initialiseRequestHeaders()
        # Whether or not we are logged in
        self.loggedIn = False

    async def createAccount(self):
        #await self._startSession()
        await self._autoLogin()
        url = self.url+'/service/users/signup'
        data = {}
        data['id'] = await self._getGuid()
        data['social_id'] = ''
        data['social_name'] = ''
        data['image'] = ''
        data['country_code'] = 'AU'
        data['country'] = 'Australia'
        data['email'] = self.user.email
        data['first_name'] = self.user.firstName
        data['last_name'] = self.user.lastName
        data['username'] = self.user.username
        data['password'] = self.user.password
        data['confirm_password'] = self.user.retypedPassword
        data['gender'] = ''
        data['csrf_token'] = self.csrf_token
        #mode = 1 allows us to create an account without having to activate it via email.
        data['mode'] = '1'
        try:
            response_headers = await self.session.post(url, headers = self.headers, data = data)

            try:
                response_json = await response_headers.json(content_type='text/html')
            except:
                raise RuntimeError("Request failed with error code: %s" % response_headers.status)
        except:
            raise
        return response_json

    async def login(self):
        url = self.url+'/service/users/login'
        data = {}
        data ['username'] = self.user.username
        data['password']  = self.user.password
        data ['password_token'] = await self._getGuid()
        data['csrf_token'] = self.csrf_token
        data['remember_me'] = '1'
        try:
            response_headers = await self.session.post(url, headers=self.headers, data=data)
            response_json = await response_headers.json(content_type='text/html')
            self._checkResponseForError(response_json)
            self.loggedIn = True
        except:
            raise
        return response_json

    async def addItem(self, item):
        if not self.loggedIn:
            raise RuntimeError("You are not logged in. You must login before adding an item.")
        url = self.url+'/service/items/additem'
        headers = self.headers
        headers['Referer'] = "%s/%s/additem"%(self.url, self.user.username)
        guid  = await self._getGuid()
        data = {}
        data['csrf_token'] = self.csrf_token	
        data['current_friend'] = ''
        data['events'] = ''
        data['file_name'] = ''
        data['friends[]'] = '0'
        data['image_from'] = ''
        data['item_category'] = ''
        data['item_desc']     = item.description
        data['item_id'] = guid
        data['item_image'] = '/images/icons/blank-item.png'
        data['item_name'] = item.itemName
        data['item_price'] = item.price
        data['item_qty']   = item.qty
        data['original_item_id'] = guid
        data['privacy'] = item.privacy
        try:
            response_headers = await self.session.post(url, headers = headers, data = data)
            response_json = await response_headers.json(content_type='text/html')
            self._checkResponseForError(response_json)
        except:
            raise
        return response_json
    '''   
    def addFriend(self, friend):
        if not self.loggedIn:
            raise RuntimeError("You are not logged in. You must login before adding a friend.")
        url = self.url+'/service/friends/addfriend'
        headers = self.headers
        headers['Referer'] = "%s/%s/addfriend"%(self.url, self.user.username)
        data = {}
        data['csrf_token'] = self.csrf_token	
        data['notification_id'] = self._getGuid()
        data['first_name'] = friend.firstName
        data['last_name'] = friend.lastName
        data['email'] = friend.email
        data['invite'] = '0'
        data['who_id'] = self._getGuid()
        try:
            response = requests.post(url, headers = headers, data = data, cookies = self.cookies)
            self._checkResponseForError(response)  
        except:
            raise
        return response.json()    
    '''
    async def _getGuid(self):
        url = self.url+'/service/tools/getguid'
        data = {'csrf_token' : self.csrf_token}
        try:
            response_headers = await self.session.post(url, headers = self.headers, data = data)
            response_json = await response_headers.json(content_type='text/html')
            self._checkResponseForError(response_json)
        except:
            raise  
        return  response_json['data']['guid']

    '''   
    def _getGuids(self):
        url = self.url+'/service/tools/getguid'
        data = {'csrf_token' : self.csrf_token}
        try:
            response = requests.post(url, headers = self.headers, data = data, cookies = self.cookies)
            self._checkResponseForError(response)  
        except:
            raise
        return response.json()['data']['guids']
        
    '''
    async def _autoLogin(self):
        url = self.url+'/service/users/autologin'
        self.cookies = {}
        self.cookies['magicaltourstop'] = '1'
        self.cookies['magicalStopTour'] = '1'
        self.session = aiohttp.ClientSession(cookies = self.cookies)
        data = {'csrf_token' : ''}

        try:
            response_headers = await self.session.post(url, headers = self.headers, data = data)
            response_json = await response_headers.json(content_type='text/html')
            #self._checkResponseForError(response_json)
        except:
            raise
        self.csrf_token = response_headers.cookies['csrf_token']
        return response_json
        
    async def _startSession(self):
        url = self.url+'/service/users/startsession'
        self.cookies = {}
        self.cookies['magicaltourstop'] = '1'
        self.cookies['magicalStopTour'] = '1'
        self.session = aiohttp.ClientSession(cookies = self.cookies)
        data = {'csrf_token' : ''}
        try:
            response_headers = await self.session.post(url, headers = self.headers)
            response_json = await response_headers.json(content_type='text/html')
            self._checkResponseForError(response_json)
        except:
            raise
        return response_json
        
    def _initialiseRequestHeaders(self):
        self.headers = {}
        self.headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        self.headers['Accept-Encoding'] = 'gzip, deflate, br'
        self.headers['Accept-Language'] = 'en-US,en;q=0.8'
        self.headers['Connection'] = 'keep-alive'
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        self.headers['Host'] = "%s.%s"%(self.site, self.domain)
        self.headers['Origin'] = self.url
        self.headers['Referer'] = self.url
        self.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        self.headers['X-Requested-With'] = 'XMLHttpRequest'
        
    def _checkResponseForError(self,response):
        try:
            if response['status'] != 1:
                raise RuntimeError("%s"%response)
        except:
            raise RuntimeError(response)