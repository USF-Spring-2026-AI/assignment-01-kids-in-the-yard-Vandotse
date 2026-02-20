# AI Assignment 01 - Kids in the Yard


## Comparison

### Which tool(s) did you use?

ChatGPT 5.2

### If you used an LLM, what was your prompt to the LLM?

I pasted in the requirements and added the necessary CSV files as a reference. I wrote the following message:

Complete the assignment based on the requirements. I have attached the CSV files as reference. Use the Python style standard called PEP 8.

### What differences are there between your implementation and the LLM?

One of the main differences was that the LLM added a lot of checks to make sure the data was valid or existed. Since I knew my data and that we would only be using CSV files with correct data, I was not worried about malicious or imperfect entries. The LLM accounted for this and added various error checking.

### What changes would you make to your implementation in general based on suggestions from the LLM?

I think adding some error checks or validation to ensure the data is valid is a good idea that I had not incorporated much in my implementation.

### What changes would you refuse to make?

Instead of throwing an error when it detected non-valid entries, the LLM added "fallback" or "default" values to use. This does not seem like a very stable fix and could lead to more problems.
