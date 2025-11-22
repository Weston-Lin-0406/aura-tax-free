import { ErrorResponse } from "../class/ErrorResponse.js";

const instance = axios.create();

// before request
instance.interceptors.request.use(config => {
	if (config.url == '/login' && config.method == 'post') {
		return config;
	}

	const token = sessionStorage.getItem('accessToken');
	if (token) {
		config.headers = config.headers || {};
		config.headers['Authorization'] = `Bearer ${token}`;
	} else {
		window.location.href = '/login';
	}
	return config;
}, error => Promise.reject(error));

// before response
instance.interceptors.response.use(
	res => {
		if (res.status == 200) {

			// if get and 200 return data object
			if (res.config.method == 'get' && res.headers['content-type'] == 'application/json') {
				return res.data.data;
			}

		}
		
		return res;
	},
	err => {
		console.log(err);
		const errRes = new ErrorResponse(err, false);
		if (errRes.status == 401 && errRes.detail.startsWith('token')) {
			errRes.detail = '帳號過期，請重新登入';
		}
		
		if (errRes.status == 422) {
			errRes.detail = 'Request failed with status code 422';
		}

		if (errRes.status == 500) {
			errRes.detail = '系統錯誤';
		}
		
		return Promise.reject(errRes);
	}
);

export default instance;