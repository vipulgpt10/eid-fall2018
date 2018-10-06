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



/* Import node-dht-sensor module */
var sensor = require('node-dht-sensor');

var cnt = 0;

/* Arrays for storing 10 reading samples */
var temp_list = [];
var hum_list = [];

/* Sum function */
function getSum(a, b)
{
    return a + b;
}

/* Read temperature and humidity */
function temp_humd(err, temperature, humidity)
{
	/* Check when valid readings */
	if (!err) 
	{
		/* Convert degC to degF */ 
		var temp_f = (temperature * 9/5) + 32.0 ;
		cnt++;
		
		console.log(cnt + ' - ' +  'Temp: ' + temp_f.toFixed(1) + ' degF, ' +
			humidity.toFixed(1) + '% Hum');
		
		/* add to the array */
		temp_list.push(temp_f);
		hum_list.push(humidity);
		
	}
}


function intervalFunc() 
{
	/* Read sensor readings */
	sensor.read(22, 4, temp_humd);
	
	if(cnt == 10)
	{
		cnt = 0;
		
		/* Calculate array sum */
		var temp_sum = temp_list.reduce(getSum);
		var hum_sum = hum_list.reduce(getSum);
		
		console.log('-------------------------------------');
		
		/* Calculate minimum */
		console.log('Lowest Temp: ' + (Math.min(...temp_list)).toFixed(1));
		console.log('Lowest Hum: ' + (Math.min(...hum_list)).toFixed(1));
		
		/* Calculate maximum */
		console.log('Highest Temp: ' + (Math.max(...temp_list)).toFixed(1));
		console.log('Highest Hum: ' + (Math.max(...hum_list)).toFixed(1));
		
		/* Calculate average */
		console.log('Average Temp: ' + (temp_sum/10).toFixed(1));
		console.log('Average Hum: ' + (hum_sum/10).toFixed(1));
		
		console.log('-------------------------------------');
		
		/* Clear arrays */
		temp_list = [];
		hum_list = [];
	}
}

/* Infinite loop at every 1 sec */
setInterval(intervalFunc, 1000);
