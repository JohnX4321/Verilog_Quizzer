module adder (
    input a,
    input b,
    input c,
    output sum,
    output carry
);

assign sum = a^b^c;
assign carry = a&b | b&c | a&c;
endmodule

