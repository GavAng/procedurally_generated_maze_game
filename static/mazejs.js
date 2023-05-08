function updateGame(direction){ //updates the room the player is currently in
	
	const rooms = document.getElementsByClassName("room");
	var playerPosition = document.getElementById("position").innerHTML;
	var currentRoom = rooms[playerPosition - 1];
	var finishPosition = document.getElementById("finishPosition").innerHTML;

    var moveBool = false;
	
	
	if(direction == 0){
		
		if(currentRoom.getElementsByTagName("north")[0].innerHTML != 0){
			var newPlayerPosition = currentRoom.getElementsByTagName("north")[0].innerHTML;
            var moveBool = true;
		}
	}
	
	else if(direction == 1){
		
		if(currentRoom.getElementsByTagName("east")[0].innerHTML != 0){
			var newPlayerPosition = currentRoom.getElementsByTagName("east")[0].innerHTML;
            var moveBool = true;
		}
	}
		
	else if(direction == 2){
		
		if(currentRoom.getElementsByTagName("south")[0].innerHTML != 0){
			var newPlayerPosition = currentRoom.getElementsByTagName("south")[0].innerHTML;
            var moveBool = true; 
		}
	}
	
	else if(direction == 3){
		
		if(currentRoom.getElementsByTagName("west")[0].innerHTML != 0){
			var newPlayerPosition = currentRoom.getElementsByTagName("west")[0].innerHTML;
            var moveBool = true;
		}
	}
	
	else{
		var newPlayerPosition = 1;
        var moveBool = true;
	}
	
	
	if(moveBool){
		console.log("True")
		lightLevelsRevert(rooms);

		var newRoom = rooms[newPlayerPosition - 1];
		newRoom.style.backgroundColor = "#91F291";

		lightLevelsRender(rooms,newRoom);
		document.getElementById("position").innerHTML = newPlayerPosition;

		torchRender(rooms);
		finishRender(rooms);

		movementUpdater(newPlayerPosition);


		if(newPlayerPosition == finishPosition){ //if game is finished
			finishProtocol();
		}
	}
	else{
		document.getElementById("movementLog").innerHTML = "You hit a wall.";
	}
}





function lightLevelsRender(rooms,firstRoom){

    const secondRooms = lightLevelsChange(rooms,firstRoom,"#D0D0D0");


    if(secondRooms.length != 0){
        
        for (var secondIndex = 0; secondIndex < secondRooms.length; secondIndex++){

            var secondRoom = secondRooms[secondIndex];
            const thirdRooms = lightLevelsChange(rooms,secondRoom,"#707070");


            if(thirdRooms.length != 0){

                for (var thirdIndex = 0; thirdIndex < thirdRooms.length; thirdIndex++){

                    var thirdRoom = thirdRooms[thirdIndex];
                    const fourthRooms = lightLevelsChange(rooms,thirdRoom,"#505050");


                    if(fourthRooms.length != 0){

                        for (var fourthIndex = 0; fourthIndex < fourthRooms.length; fourthIndex++){

                            var fourthRoom = fourthRooms[fourthIndex];
                            lightLevelsChange(rooms,fourthRoom,"#000000");
                        }
                    }
                }
            }
        }
    }
}





function lightLevelsChange(rooms,currentRoom,lightLevel){

    const directions = ["north","east","south","west"];
    const nextRooms = [];


    for (var index = 0; index < 4; index++){

        var currentDirection = directions[index];


        if(currentRoom.getElementsByTagName(currentDirection)[0].innerHTML != 0){

            var nextRoomPosition = currentRoom.getElementsByTagName(currentDirection)[0].innerHTML;
            var nextRoom = rooms[nextRoomPosition - 1];
            var nextRoomColour = rgbToHex(nextRoom.style.backgroundColor); //converts standard rgb value into hex value (hex value allows lexicographic comparisons)


            if(nextRoomColour != "#91f291" && nextRoomColour != "#ffaa00"){

                if(lightLevel > nextRoomColour){

                    nextRoom.style.backgroundColor = lightLevel;
                    
                    nextRooms.push(nextRoom);
                }
            }


            if(rgbToHex(nextRoom.style.backgroundColor) != "#000000"){ 
                wallLightLevelsChange(currentRoom,nextRoom,currentDirection);
            }
            else{ //if next room colour is still black
                wallLightLevelsDarken(currentRoom,nextRoom,currentDirection);
            }
        }
    }


    return nextRooms;
}





function wallLightLevelsDarken(firstRoom,secondRoom,direction){

    if(direction == "north"){
        firstRoom.style.borderTopColor = "black";
        secondRoom.style.borderBottomColor = "black";
    }
    else if(direction == "east"){
        firstRoom.style.borderRightColor = "black";
        secondRoom.style.borderLeftColor = "black";
    }
    else if(direction == "south"){
        firstRoom.style.borderBottomColor = "black";
        secondRoom.style.borderTopColor = "black";
    }
    else{
        firstRoom.style.borderLeftColor = "black";
        secondRoom.style.borderRightColor = "black";
    }
}





function wallLightLevelsChange(firstRoom,secondRoom,direction){

    var firstColour = rgbToHex(firstRoom.style.backgroundColor); //converts standard rgb value into hex value (hex value allows lexicographic comparisons)
    var secondColour = rgbToHex(secondRoom.style.backgroundColor);


    if(direction == "north"){
        firstRoom.style.borderTopColor = firstColour;
        secondRoom.style.borderBottomColor = secondColour;
    }
    else if(direction == "east"){
        firstRoom.style.borderRightColor = firstColour;
        secondRoom.style.borderLeftColor = secondColour;
    }
    else if(direction == "south"){
        firstRoom.style.borderBottomColor = firstColour;
        secondRoom.style.borderTopColor = secondColour;
    }
    else{
        firstRoom.style.borderLeftColor = firstColour;
        secondRoom.style.borderRightColor = secondColour;
    }
}





function lightLevelsRevert(rooms){ //sets all the light levels back to darkness

    for (var index = 0; index < rooms.length; index++) {

        var currentRoom = rooms[index];
        currentRoom.style.backgroundColor="#000000";
        currentRoom.style.borderTop="2px solid #000000";
        currentRoom.style.borderRight="3px solid #000000";
        currentRoom.style.borderBottom="2px solid #000000";
        currentRoom.style.borderLeft="3px solid #000000";
    }

}





function placeTorch(){ //sets or removes the attribute torch position

	var playerPosition = document.getElementById("position").innerHTML;
    var torchPosition = document.getElementById("torchPosition").innerHTML;


    if(torchPosition == 0){
        document.getElementById("torchPosition").innerHTML = playerPosition
        document.getElementById("spacebar").getElementsByTagName("p")[0].innerHTML = "Pickup Torch";
    }
    else if(torchPosition == playerPosition){
        document.getElementById("torchPosition").innerHTML = 0;
        document.getElementById("spacebar").getElementsByTagName("p")[0].innerHTML = "Place Torch";
    }
}





function torchRender(rooms){ //renders the torch and its effects

    var playerPosition = document.getElementById("position").innerHTML;
    var torchPosition = document.getElementById("torchPosition").innerHTML;


    if(torchPosition != 0){

        var torchRoom = rooms[torchPosition - 1]


        if(torchPosition != playerPosition){ //if current room is not player room
            torchRoom.style.backgroundColor = "#FFAA00";
        }


        lightLevelsRender(rooms,torchRoom)
    }
}





function finishProtocol(){
    document.getElementById("stopGame").innerHTML = 1;
    document.getElementById("controls").style.display="none";

    document.getElementById("formTime").value = document.getElementById("timer").innerHTML;
    document.getElementById("formMovementCount").value = parseInt(document.getElementById("movementCountDisplay").innerHTML) + parseInt(document.getElementById("totalMoves").innerHTML);
    
    document.getElementById("gameFormSubmit").style.display="block";
}





function finishRender(rooms){ //renders the finish room

    var finishPosition = document.getElementById("finishPosition").innerHTML;
    var finishRoom = rooms[finishPosition - 1];
    var finishRoomColour = rgbToHex(finishRoom.style.backgroundColor);


    if(finishRoomColour == "#d0d0d0"){
        finishRoom.style.backgroundColor = "#EB3636";
    }
    else if(finishRoomColour == "#707070"){
        finishRoom.style.backgroundColor = "#9B2323";
    }
    else if(finishRoomColour == "#505050"){
        finishRoom.style.backgroundColor = "#5E1717";
    }


    const directions = ["north","east","south","west"];


    for (var index = 0; index < 4; index++){

        var currentDirection = directions[index];


        if(finishRoom.getElementsByTagName(currentDirection)[0].innerHTML != 0){

            var nextRoomPosition = finishRoom.getElementsByTagName(currentDirection)[0].innerHTML;
            var nextRoom = rooms[nextRoomPosition - 1];

            wallLightLevelsChange(finishRoom,nextRoom,currentDirection);
        }
    }
}





function movementUpdater(roomPosition){

    var movementCount = document.getElementById("movementCount").innerHTML;


    if(movementCount != 0){
        document.getElementById("movementLog").innerHTML = "You entered room " + roomPosition + ".";
    }

    document.getElementById("movementCountDisplay").innerHTML = movementCount;

    movementCount++;
    document.getElementById("movementCount").innerHTML = movementCount;

    if(movementCount == 2){
        setInterval(timer,100);
    }
}





function timer(){
	
    var time = document.getElementById("timer").innerHTML;
    var seconds = parseInt(time.substring(0,3));


    if(seconds == 100){ //end game if player takes 100 seconds
        finishProtocol();
    }


    var stopGame = document.getElementById("stopGame").innerHTML;
	
	
	if(stopGame == 0){

		var seconds = parseInt(time.substring(0,2));
		var tenthSeconds = parseInt(time.substring(5));

		tenthSeconds++;


		if(tenthSeconds == 10){
			var tenthSeconds = 0;
			seconds++;
		}


		if(seconds < 10){
			var seconds = "0" + seconds;
		}


		var time = seconds + " . " + tenthSeconds;
		document.getElementById("timer").innerHTML = time;
	}
}





window.addEventListener("keydown", function (event) {
    if (event.defaultPrevented) {
      return; // Do nothing if the event was already processed
    }
	
	var stopGame = document.getElementById("stopGame").innerHTML;
  
    switch (event.key) {
      case "ArrowDown":
		if(stopGame == 0){
			updateGame(2);
		}
        break;
      case "ArrowUp":
        if(stopGame == 0){
			updateGame(0);
		}
        break;
      case "ArrowLeft":
        if(stopGame == 0){
			updateGame(3);
		}
        break;
      case "ArrowRight":
        if(stopGame == 0){
			updateGame(1);
		}
        break;
      default:
        return; // Quit when this doesn't handle the key event.
    }
  
    // Cancel the default action to avoid it being handled twice
    event.preventDefault();
  }, true);

document.addEventListener('keydown', (e) => {
    if (e.code === "Space") {
        placeTorch();
    }
});





function rgbComponentGetter(rgb){ //semi self coded - splits rgb value into r g b colour components
    rgbString = rgb.replace(/[^\d,]/g, '').split(',');
    rgbInt = rgbStringToInt(rgbString);


    return rgbInt
}

function rgbStringToInt(rgbArray){ //self coded - converts rgb string values to integers

    for (var index = 0; index < 3; index++){

        rgbArray[index] = parseInt(rgbArray[index])
    }


    return rgbArray
}

function componentToHex(component) { //copied
    var hex = component.toString(16);


    return hex.length == 1 ? "0" + hex : hex;
}
  
function rgbToHex(rgb) { //semi self coded - converts standard rgb value into hex value (hex value allows lexicographic comparisons))
    rgbComponents = rgbComponentGetter(rgb);


    return "#" + componentToHex(rgbComponents[0]) + componentToHex(rgbComponents[1]) + componentToHex(rgbComponents[2]);
}





function optionChange(optionBox){
    optionBox.getElementsByClassName("optionHeading")[0].style.textDecoration="underline";
    optionBox.getElementsByClassName("optionHeading")[0].style.textDecorationThickness="0.045em";

    optionBox.getElementsByClassName("optionText")[0].style.display="block";
}
function optionRevert(optionBox){
    optionBox.getElementsByClassName("optionHeading")[0].style.textDecoration="initial";
    optionBox.getElementsByClassName("optionText")[0].style.display="none";
}





function updateFinishForm(){
	if(document.querySelector('input[name="saveResults"]:checked').value == "yes"){
		document.getElementById("usernameInput").style.display="block";
	}
	else{
		document.getElementById("usernameInput").style.display="none";
		document.getElementById("username").value = "";
		document.getElementById("warning").style.display="none";
	}
}





function finishFormSubmit(){

	if(document.querySelector('input[name="saveResults"]:checked').value == "no" ||
	(document.querySelector('input[name="saveResults"]:checked').value == "yes" && 
	usernameVerify())){
		
		document.getElementById("finishForm").submit();
	}
	

    else{
        document.getElementById("warning").style.display="block";
    }
}





function usernameVerify(){

    const currentUsername = document.getElementById("username").value;


    if(currentUsername == ""){
        document.getElementById("warning").innerHTML = "Enter a username to be submitted.";
        return false
    }


    for (let i = 0; i < currentUsername.length; i++){
        if(currentUsername[i] == ","){
            document.getElementById("warning").innerHTML = 'Username cannot contain ",".';
            return false
        }
    }


    if(document.getElementById("takenUsernames").innerHTML != 0){

        const takenUsernames = document.getElementById("takenUsernames").innerHTML.split(",");


        if(takenUsernames[0] != 0){
            if(takenUsernames.includes(currentUsername)){
                document.getElementById("warning").innerHTML = "Username already taken.";
                return false
            }
        }
    }


    return true
}