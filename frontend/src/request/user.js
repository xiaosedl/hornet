import request from '@/HttpCommon.js'


class UserApi {

    login(data) {
        return request.post('/api/users/login', data)
    }

    logout(data) {
        return request.post('/api/users/logout', data)
    }

    register(data) {
        return request.post('/api/users/register', data)
    }
}


export default new UserApi()