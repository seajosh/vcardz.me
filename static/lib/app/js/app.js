/*global  */
(function() {
  var app = angular.module('vcardz', []);

  // // http://stackoverflow.com/questions/23885018/cannot-catch-event-in-angularjs-controller
  app.config(function ($provide) {
    // Define an alternative to $rootScope.$on. 
    // $scope.subscribe will emulate the same behaviour, with the difference
    // of removing the event listener when $scope.$destroy is called. 
    $provide.decorator('$rootScope', function ($delegate) {
      Object.defineProperty($delegate.constructor.prototype, 'subscribe', {
        value: function (name, listener) {
          var unsub = $delegate.$on(name, listener);
          this.$on('$destroy', unsub);
        },
        enumerable: false
      });

      return $delegate;
    });
  });


  var factoryPubsub = function($rootScope) {
    var security = {
        login: function() {
            $rootScope.$emit('login');
        },

        onLogin: function($scope, handler) {
          $scope.$on('login',
                     function(event) {
                       handler(event);
                     });
        }

    };

    var data = {
        load: function() {
          $rootScope.$emit('data:load');
        },

        onLoad: function($scope, handler) {
          $scope.$on('data:load',
                     function(event, data) {
                       handler(event);
                     });
        }
    };

    var service = {};
    service.security = security;
    service.data = data;
    return service;
  }
  app.factory('pubsub', ['$rootScope', factoryPubsub]);


  var dataService = function() {
    this.cards = [];
  };
  app.service('dataBus', dataService);


  app.directive('loginGoogle',
                ['pubsub',
                function(pubsub) {
                  var controller = function($scope, $window, $http) {

                    $scope.hide_login = false;

                    $scope.renderLogin = function() {
                      console.log('login.render');
                      // Additional params
                      var params = {
                        'accesstype': 'offline',
                        'callback': $scope.loginCallback,
                        'clientid': '710958114554-4ovgk8nmv0nk0d4q2g177f747mfukl4p.apps.googleusercontent.com',
                        'cookiepolicy': 'single_host_origin',
                        'requestvisibleactions': 'http://schema.org/AddAction',
                        'scope': 'https://www.googleapis.com/auth/plus.login https://www.googleapis.com/auth/contacts.readonly'
                      };
                      gapi.signin.render('googleLogin', params);
                    };

                    $scope.loginCallback = function (authResult) { 
                      // console.log(JSON.stringify(authResult));
                      // console.log(authResult.code);
                      if (authResult['status']['signed_in']) 
                      {
                        $http
                        .post('/rest/v1/google/signin',
                              JSON.stringify(authResult.code))
                        .success(function(data, status) {
                          $scope.hide_login = true;
                          console.log('signin post successful');
                          pubsub.security.login();
                        });

                      } 
                      else 
                      {
                        // Update the app to reflect a signed out user
                        // Possible error values:
                        //   "user_signed_out" - User is signed-out
                        //   "access_denied" - User denied access to your app
                        //   "immediate_failed" - Could not automatically log in the user
                        console.log('Sign-in state: ' + authResult['error']);
                      }
                    };

                    $scope.start = function() {
                      $scope.renderLogin();
                    };
                    $window.google_login = $scope.start;

                    $scope.$on('login',
                               function() {console.log('cow horse');});

                  };

                  return {
                    restrict: 'E',
                    templateUrl: '/lib/app/templates/login/login.html',
                    controller: controller
                  };
                }]);


  app.directive('fetchData',
                ['pubsub',
                 'dataBus',
                 function(pubsub, dataBus) {

                   var controller = function($scope, $http) {
                     $scope.hide_loading = true;

                     $scope.loadContacts = function() {
                       $http
                       .get('/rest/v1/google/contacts')
                       .success(function(data, status) {
                         console.log(data);
                         dataBus.cards = data;
                         pubsub.data.load();
                       });
                     };
                   };

                   var link = function($scope, element, attr) {
                     var onLogin = function() {
                         console.log('fetch-data => onLogin');
                         $scope.hide_loading = false;
                         $scope.loadContacts();                       
                     };
                     pubsub.security.onLogin($scope, onLogin);

                     var onDataLoad = function() {
                       $scope.hide_loading = true;
                     };
                     pubsub.data.onLoad($scope, onDataLoad);
                   };

                   return {
                     restrict: 'E',
                     templateUrl: '/lib/app/templates/fetch/fetchData.html',
                     controller: controller,
                     link: link
                   };

                 }]);

  app.directive('vcardList',
                ['pubsub',
                 'dataBus',
                 function(pubsub, dataBus) {

                   var controller = function($scope) {
                     $scope.cards = [];

                     $scope.rip = function() {
                       $scope.cards = dataBus.cards;
                     };

                   };

                   var link = function($scope, element, attr) {
                     var onDataLoad = function(data) {
                       console.log('vcard-list => onDataLoad');
                       $scope.rip();
                     };
                     pubsub.data.onLoad($scope, onDataLoad);
                   };

                   return {
                     restrict: 'E',
                     templateUrl: '/lib/app/templates/fetch/vcardList.html',
                     controller: controller,
                     link: link
                   };
                 }]);
  
  app.controller('LoginController', function() {
    this.providers = [
      {
        'name': 'Google'
      }];
  });


})();