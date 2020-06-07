function confirmCheck()//checks if you are sure you want to add proceeed
	{
		var response;
		response = confirm('Are all details correct do you want to proceed?');
		if(response){
				
			return true;
		}
		else{
			return false;
			}
}
