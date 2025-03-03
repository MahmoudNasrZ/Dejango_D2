// document.addEventListener("DOMContentLoaded", function () { 
// // DomContentLoaded Ensure that it is loaded after HTML document is loaded
// The Native One 
//     input = document.querySelector(".inputToTest");
//     let i = 0
// setInterval(function () {
// let inputToChange = ["Math101","Science102","History201"]
// if (i<inputToChange.length) {
//     input.value = inputToChange[i]
//     i++
//     console.log(input.value);
    
// } else {
//     i=0
// }


// },2000)
// });
/////////////////////////////////////////////
  window.onload = function() {
    console.log("Everything, including images, is loaded!");

    // The Middle AgedOne
    const input = document.querySelector(".inputToTest");
    const inputToChange = ["Math101", "Science102", "History201"];
    let i = 0;

    function updateInput() {
        // in Case you don't Know JavaScript Event Loop it first Executes EverySync function or 
        // command(CallStack) Then gose the (CallBackQueue)==>That is consistent Of microTask and MacroTask
        // MicroTask like  Promise Async next-tick etc  Higher level(priority queue)
        //MacroTask like Settimout setinterval etc 
        setTimeout(updateInput, 2000); // 4TH Recursive timeout instead of setInterval 
        input.value = inputToChange[i]; // 1ST
        console.log(input.value); // 2ND
        i = (i + 1) % inputToChange.length; //3RD Loop back to 0 when reaching the end  I=0 ==> I + 1 = 1 % 3 = 1 ETC 3%3 = 0
    }

    updateInput(); // Start the loop
}

// document.addEventListener("DOMContentLoaded", async function () {
// The Modern One 
//     const input = document.querySelector(".inputToTest");
//     const inputToChange = ["Math101", "Science102", "History201"];
    
//     let i = 0;
//     while (true) {
//         await new Promise(resolve => setTimeout(resolve, 2000)); //4th Why  3shan De al Event Loop in JavaScript
//         input.value = inputToChange[i]; // First
//         console.log(input.value); //2nd
//         i = (i + 1) % inputToChange.length; //3rd I=0 ==> I + 1 = 1 % 3 = 1 ETC 3%3 = 0
//     }
// });
