function test1() {
	document.getElementById("demo1").addEventListener('click', function() {
		console.log("test1");
	})
}

function test2() {
	alert("test2");
}

function test3() {
	document.getElementById("demo3").addEventListener('click', function() {
		console.log("test3");
	})
}

// if (document.readyState === "loading") {
	// document.addEventListener("DOMContentLoaded", test2);
	document.addEventListener("DOMContentLoaded", test1);
//   } 
	// test2();
//   }

test3();