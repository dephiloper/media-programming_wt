let calculator = (function () {
   let currentNumber = 0;

   return {
        add : (x) => currentNumber += x,
        sub : (x) => currentNumber -= x,
        mul : (x) => currentNumber *= x,
        div : (x) => currentNumber /= x,
        toString : () => currentNumber,
        reset : () => currentNumber = 0,
   }
}());

calculator.add(3);
console.log(calculator);
calculator.sub(-9);
console.log(calculator);
calculator.mul(5);
console.log(calculator);
calculator.div(6);
console.log(calculator);
calculator.reset();
console.log(calculator);

