`timescale 1ns/1ns
//`include "soln.v"

module tb_adder();

reg a,b,c;
wire sum,carry;
reg[1:0] case_number;
reg [2:0] tk = 0;
reg clk;
integer file;
localparam cycle = 10;

initial begin
    clk = 0;
    forever #(cycle/2) clk = ~clk; 
end

adder uut (.a(a), .b(b), .c(c), .sum(sum), .carry(carry));

initial begin

    file = $fopen("output.txt","w");
    $dumpfile("tb_adder.vcd");
    $dumpvars(0,tb_adder);
    
    #5 case_number = 2'd0;
    a =1;
    b = 1;
    c = 1;
    #10 case_number = 2'd1;
    a=1;
    b = 0;
    c = 1;
    #10 case_number = 2'd2;
    a = 0;
    b = 0;
    c = 0;
    #10 case_number = 2'd3;
    a = 0;
    b = 1;
    c = 0;
    #10 case_number = 2'dx;
    #20 $fclose(file); 
    $finish;
end

always@(negedge clk)
    case (case_number)
        2'd0: if(sum == 1 && carry == 1)
                begin
                $fdisplay(file,"Test 1 => Passed");
                tk = tk + 1;
                end
            else
                begin
                $fdisplay(file,"Test 1 => Failed"); 
                tk = tk + 0;
                end
        2'd1: if(sum == 0 && carry == 1)
                begin
                $fdisplay(file,"Test 2 => Passed");
                tk = tk + 1;
                end
            else
                begin
                $fdisplay(file,"Test 2 => Failed"); 
                tk = tk + 0;
                end
        2'd2: if(sum == 0 && carry == 0)
                begin
                $fdisplay(file,"Test 3 => Passed");
                tk = tk + 1;
                end
            else
                begin
                $fdisplay(file,"Test 3 => Failed"); 
                tk = tk + 0;
                end
        2'd3: if(sum == 1 && carry == 0)
                begin
                $fdisplay(file,"Test 4 => Passed");
                tk =tk + 1;
                end
            else
                begin
                $fdisplay(file,"Test 4 => Failed"); 
                tk = tk + 0;
                end
        default: tk = tk + 0;
    endcase
always@(case_number)
    if(case_number == 2'd3)
            #10  $fdisplay(file,"\nNumber of Tests Passed - %d\nNumber of Tests Failed - %d",tk, (3'd4-tk));
endmodule