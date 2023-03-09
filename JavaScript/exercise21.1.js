// Exercise 22.1, arrays, indexering
let foo = ["Charlie", "bella", "jimi", "lundis"]
console.log("Det här är tredje namnet i arrayen: " + foo[2])

// If-satser
let name = "Jennifer"
if (name == "Jennifer") {
    console.log("Thats my name too!")
}


let myVariable = 8
if (myVariable > 5) {
    console.log("upper")
}
else{
    console.log("lower")
}

// For-loops
for(var i = 0; i < 2; i++) {  
    console.log(i);
    }

var items = ["foo", "bar", "baz"]; // First we create an array.
for( var i = 0; i < items.length; i++ ) {
console.log(items[i]); // This will alert each item in the array.
}