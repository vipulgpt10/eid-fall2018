/*
 * HW 4 - EID - Vipul Gupta
 * 
 * node.js version: v10.11.0
 * 
 * ref: https://www.w3schools.com/js/
 * https://weworkweplay.com/play/raspberry-pi-nodejs/
 * https://github.com/momenso/node-dht-sensor
 * https://nodejs.org/en/docs/guides/timers-in-node/
 * 
*/




var sensor = require('node-dht-sensor');

var cnt = 0;

var temp_list = [];
var hum_list = [];


function getSum(a, b)
{
    return a + b;
}

function temp_humd(err, temperature, humidity)
{
	if (!err) 
	{
		var temp_f = (temperature * 9/5) + 32.0 ;
		cnt++;
		
		console.log(cnt + ' - ' +  'Temp: ' + temp_f.toFixed(1) + ' degF, ' +
			humidity.toFixed(1) + '% Hum');
		
		temp_list.push(temp_f);
		hum_list.push(humidity);
		
		
	}
}


function intervalFunc() 
{
	//console.log('Cant stop me now!');
	sensor.read(22, 4, temp_humd);
	
	if(cnt == 10)
	{
		cnt = 0;
		var temp_sum = temp_list.reduce(getSum);
		var hum_sum = hum_list.reduce(getSum);
		
		console.log('-------------------------------------');
		
		console.log('Lowest Temp: ' + (Math.min(...temp_list)).toFixed(1));
		console.log('Lowest Hum: ' + (Math.min(...hum_list)).toFixed(1));
		
		console.log('Highest Temp: ' + (Math.max(...temp_list)).toFixed(1));
		console.log('Highest Hum: ' + (Math.max(...hum_list)).toFixed(1));
		
		console.log('Average Temp: ' + (temp_sum/10).toFixed(1));
		console.log('Average Hum: ' + (hum_sum/10).toFixed(1));
		
		console.log('-------------------------------------');
		
		temp_list = [];
		hum_list = [];
		
	}

}

setInterval(intervalFunc, 1000);
