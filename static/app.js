(function(){

angular.module('HelloApp', [])
.controller('HelloController', HelloController)
.service('HelloService', HelloService);


/************************************************************/
HelloService.$inject = ['$http', 'API'];
function HelloService($http, API) {
  var svc = this;

  svc.getHellos = function() {
    return $http.get(API + '/api/hello'
    ).then(function(result){
      return result.data.result;
    })
  };

  svc.postHello = function(data) {
    return $http.post((API + '/api/hello'), data
    ).then(function(result){
      return result.data;
    })
  };

  svc.deleteHello = function(id) {
    return $http.delete((API + '/api/hello/' + id)
    ).then(function(result){
      return result.data;
    })
  };

}


/************************************************************/
HelloController.$inject = ['HelloService'];
function HelloController(svc) {
  var $ctrl = this;

  $ctrl.title = "Hello from";
  $ctrl.error = "";

  $ctrl.GetMsg = function(){
    var p = svc.getHellos();
    p.then(function(data){
      $ctrl.hellos = data;
    }, function(){
      $ctrl.error = "Error loading messages";
    });
  };
  $ctrl.GetMsg();

  $ctrl.AddMsg = function() {
    var p =svc.postHello({"name": $ctrl.name, "msg": $ctrl.msg});
    p.then(function(data){
      $ctrl.error = "";
      $ctrl.GetMsg();
    },function(){
      $ctrl.error = "Error posting message";
    });
  };

  $ctrl.DelMsg = function(id) {
    var p =svc.deleteHello(id);
    p.then(function(data){
      $ctrl.error = "";
      $ctrl.GetMsg();
    }, function(){
      $ctrl.error = "Error deleting message";
    });
  };


}


})()
