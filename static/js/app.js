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

	$scope.getTasks = function(){
		$http({
			url: '/tasks',
			method: 'GET',
			headers: {'Content-Type':'application/josn'}
		}).then(function(response){
			$scope.tasks = response.data.tasks;
			$scope.beforeTasksChanged = angular.copy(response.data.tasks); // makes a copy of the data for comparison
		});
	}
	$scope.enableEdit = function(data){
		console.log(data + " " + "#"+data+"_title");
		$("#"+data+"_title").removeAttr("readonly");
		$("#"+data+"_save").addClass('text-success');
		$("#"+data+"_save").show();
	}
	$scope.saveEdit = function(data){
		console.log(data + " " + "#"+data+"_title");

		$http({
			url:'/edit',
			method: 'POST',
			data: {
				'task_id':data
			}
		})


		$("#"+data+"_title").attr("readonly","readonly");
		$("#"+data+"_save").removeClass('text-success');
		$("#"+data+"_save").hide();
	}
	$scope.saveChanges = function(index,data) {
		if($scope.beforeTasksChanged[index].task_title != data.task_title || $scope.beforeTasksChanged[index].task_content != data.task_content){
			$http({
				url:'/edit',
				method: 'POST',
				data: {
				'task_id':data.task_id,
				'task_title':data.task_title,
				'task_content':data.task_content
				},
				headers: {'Content-Type':'application/json'}
			}).then(function(response){
				if(response.data.status == true){
					console.log("edited");
					$scope.tasks = response.data.tasks;
					$scope.beforeTasksChanged = angular.copy(response.data.tasks);
					// alert success and remove console log
					swal("Awesome job!", "You just edited a task!", "success")
				}
				else{
					// alert failed
					swal("Aww poop!", "We couldn't edit that task! Please try again!", "error")
				}
			})
		}
		else{
			console.log("saveChanges = False");
		}
	}
	$scope.removeTask = function(index,data){
		swal({
		  title: "Are you sure?",
		  text: "You will not be able to undo this process!",
		  type: "warning",
		  showCancelButton: true,
		  confirmButtonColor: "#DD6B55",
		  confirmButtonText: "Yes, delete it!",
		  closeOnConfirm: false
		},
		function(){
			$http({
				url:'/delete',
				method:'POST',
				data:{'task_id':data.task_id},
				headers:{'Content-Type':'application/json'}
				}).then(function(response) {
				if(response.data.status == true){
					$scope.tasks = response.data.tasks;
					$scope.beforeTasksChanged = angular.copy(response.data.tasks);
					swal("Yippee!", "You just completed/deleted a task! Way to go champ!", "success")
				}
				else{
					swal("Aww poop!", "We couldn't delete the task! Please try again!", "error")
				}
			});
		});
	}
}]);
