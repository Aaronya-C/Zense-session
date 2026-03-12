# MIPS-CA-assignment

# INTRODUCTION 

* This project emulates a MIPS Processor using a python program.
* The program takes the Binary machine code as input and runs certain instructions.
* The Assembly code is converted to Binary Machine code by the MARS Assembler developed by Pete Sanderson and Ken Vollmar
* The next section deals with the dependencies needed

# Dependencies

* The project requires the MARS assembler to run.
* However, The MARS Assembler is downloaded as a JAR(Java ARchive) file.
* Hence, Java JDK is needed

   ## Installing JDK
      * Use the following steps to download JDK (Linux based system - ubuntu)

          
              sudo apt update && sudo apt upgrade
              sudo apt install default-jdk
          

      * To verify installation use the command

        
            java --version
        

  ## Installing the MARS Assembler
      * After installing the jdk using the above method used , follow these steps to download MARS MIPS-Assembler
      * Navigate to the official git hub  repo "dpetersanderson.github.io"
      * Clone the repo
      * Then run

        

          java -jar mars4_5.jar
        

      * The assembler is ready to go



# Running the project 

* Clone the repo.
* The repo consists of Processor.py that needs to be executed to get output.
* Put your assembly code in the MARS assembler then dump the instructions and data segments seperately

* Follow these steps as shown below as shown in the pictures:

  <img width="1834" height="200" alt="image" src="https://github.com/user-attachments/assets/f72442a1-89ae-4705-81be-f4b501afa3e1" />
  <img width="750" height="661" alt="image" src="https://github.com/user-attachments/assets/d4f0989e-47d9-48ef-a0b4-bf2dcd7b99c9" />

* The print occurs after every 10 cycles. It reduces the number of line and printed




# CONTRIBUTORS

* This project has been made by freshman year students of International Institute Information Technology Bangalore (IIITB), India.
* The name of the contributors are as follows :
      Anamitra Basu
      Aaronya Chakraborty
      Aatraya Mukherjee 
  
  