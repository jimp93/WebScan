(function () {

    'use strict';

    var WebScanApp = angular.module("WebScanApp", []);

    WebScanApp.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{a');
    $interpolateProvider.endSymbol('a}');
    });

    WebScanApp.controller('WebScanController', ['$scope', '$log', '$http', '$timeout',
    function($scope, $log, $http, $timeout) {
        $scope.submitButtonText = 'Submit';
        $scope.loading = false;
        $scope.urlerror = false;

        $scope.getResults = function() {
            // get the URL from the input
            var webpage = $scope.website;
            var rtime = $scope.time;
            var numbers = $scope.numbers;
            var audio = $scope.audio;


            // fire the API request

            $http.post('/start', {'url' : webpage, 'rtime' : rtime, 'numbers' : numbers, 'audio' : audio}).
            // url checked - job sent to redis queue - job id returned - main worker function activated
              then(function(response) {
                $log.log(response);
                var jobID=response.data;
                $scope.loading = true;
                $scope.submitButtonText = 'Loading...';
                $scope.urlerror = false;
                getScan(jobID, rtime);
              },
              function(jobID) {
              });

    };

    function getScan(jobID, rtime) {

        var timeout = '';
        var jobID = jobID;
        $log.log(jobID)
        var poller = function() {
          // fire (a)nother request
            $http.post('/results', {'jobID' : jobID}).
            // if it gets to return, either completed or not completed
                then(function(data, status, headers, config) {
                  var stat = data['status'];
                  if(stat === 202) {
                    $log.log(stat);
                  } else if (stat === 200){
                      window.location = '/changed';
                      $timeout.cancel(timeout);
                      return false;
                  }
                  // continue to call the poller() function every 10 seconds
                  // until the timeout is cancelled
                  timeout = $timeout(poller, 10000);
                },
                function(error) {
                  $log.log(error);
                  $scope.loading = false;
                  $scope.submitButtonText = "Submit";
                  $scope.urlerror = true;
                });
            };
        poller();
      }
    }
  ]);

}());