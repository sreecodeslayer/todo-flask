var tApp = angular.module('todoApp', ['ngRoute'],function($interpolateProvider){
	$interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});
tApp.controller('TodoController', ['$scope', '$http', '$window', '$route', function($scope, $http, $window, $route) {
	$scope.login = function(){
		$http({
			url: '/login',
			method: 'POST',
			data: JSON.stringify({
				'username':$scope.login.username,
				'password':$scope.login.password
			}),
			headers: {'Content-Type':'application/json'}
		}).then(function(response){
			console.log(response['status'] + ' ' + response['statusText']);
			if(response.data['status'] == true){
				$window.location.reload();
			}
			else{
				console.log(response.data);
			}
		});
	}

	$scope.signup = function(){
		$http({
			url: '/signup',
			method: 'POST',
			data: JSON.stringify({
				'username':$scope.signup.username,
				'password':$scope.signup.password
			}),
			headers: {'Content-Type':'application/json'}
		}).then(function(response){
			console.log(response['status'] + ' ' + response['statusText']);
		});
	}

	$scope.logout = function(){
		$http({
			url: '/logout',
			method: 'POST',
			headers: {'Content-Type':'application/json'}
		}).then(function(response){
			console.log(response['status'] + ' ' + response['statusText']);
			if(response.data['status'] == true){
				$window.location.reload();
			}
			else{
				console.log(response.data);
			}
		});
	}
}]);
