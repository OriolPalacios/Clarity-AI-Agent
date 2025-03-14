from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

completion = client.chat.completions.create(
  extra_body={},
  model="google/gemini-2.0-pro-exp-02-05:free",
  messages=[
      {
        "role": "system",
        "content": """Paraphrase the following Question and Chain of Thought (CoT) while preserving their meaning.                   
                      You MUST return ONLY valid JSON in the exact format shown below:
                      {
                        "Question": "your rephrased question here",
                        "CoT": "your rephrased chain of thought here"
                      }
                      Do not include explanations, markdown formatting, or any text outside the JSON object."""
      },
      {
        "role": "user",
        "content": f"Question: Create a detailed Clarity smart contract for the Stacks blockchain that implements a decentralized lending protocol allowing users to deposit STX tokens, borrow against their collateral, and earn yield. The contract should include functionality for managing deposits with user-specific balances, implementing a loan system with dynamic interest calculations based on block height, and distributing yield to depositors. Incorporate a 50% loan-to-value ratio limit, a 10% interest rate, and proper error handling for various scenarios including excessive borrowing and repayment issues. Include comprehensive read-only functions for querying user balances and outstanding loan amounts, and ensure all STX transfers are handled securely using the appropriate contract-based transaction patterns. Provide detailed comments explaining the purpose and functionality of each data structure and function in the contract.\n\nCoT:" + """I'll generate a detailed Chain-of-Thought explaining the reasoning process behind the Clarity smart contract implementation.

Let's start by understanding what we need to build: a decentralized lending protocol on the Stacks blockchain with STX tokens as the primary asset. The core functionality requires deposit management, borrowing against collateral, loan processing, and yield distribution.

First, the data structure design. The contract needs to track two primary types of data: deposits and loans. For deposits, a map structure is used to associate user principals (blockchain addresses) with their deposit amounts. This approach provides user-specific accounting while maintaining the simplicity needed for a lending protocol. Similarly, loans are tracked with a separate map associating borrowers with both their loan amounts and the block height of their last interaction, which is crucial for interest calculations.

Next, global state variables are defined. The total-deposits tracks the aggregate deposits in the contract, which is necessary for calculating proportional yields. The pool-reserve holds accumulated interest payments, effectively serving as the yield source for depositors. The loan-interest-rate is set at 10% as specified in the requirements.

Error constants are defined to handle various failure scenarios, providing clear feedback to users when operations fail. This follows best practices for smart contract development where error handling is crucial for security and user experience.

Moving to the functional implementation, the deposit function allows users to add STX to the contract. It uses stx-transfer? to move tokens from the user to the contract, updates the user's balance in the deposits map, and increases the total-deposits counter. The function uses a combination of let bindings and map operations to manage state transitions safely.

The borrow function implements the 50% loan-to-value ratio requirement. It calculates the allowed borrowing limit based on half the user's deposit (/ user-deposit u2), ensuring users can't borrow more than 50% of their collateral value. Before issuing new loans, it calculates any accrued interest on existing loans using the calculate-accrued-interest private function. The function then updates the loan record with the new total and the current block height for future interest calculations.

For repayments, the repay function first calculates the total amount due including accrued interest. It then ensures users don't overpay, transfers the repayment amount to the contract, and updates the loan record. Importantly, it adds the interest portion to the pool-reserve, making it available for yield distribution.

The claim-yield function distributes accumulated interest to depositors proportionally based on their share of the total deposits. This implements the yield earning requirement in the original specification. The calculation (/ (* (var-get pool-reserve) user-deposit) (var-get total-deposits)) determines each user's fair share of the yield.

The read-only functions get-balance-by-sender, get-balance, and get-amount-owed provide transparency, allowing users to query their current positions and obligations without modifying the contract state. This supports the requirement for comprehensive query functions.

Finally, the calculate-accrued-interest private function implements the dynamic interest calculation based on block height as required. It determines the elapsed time in blocks since the last loan interaction and calculates interest proportionally. The calculation (/ (* principal (var-get loan-interest-rate) elapsed-blocks) u10000) applies the 10% interest rate over the elapsed blocks.

Wait, there seems to be an error in the borrow function. The new-loan calculation is incomplete - it only adds the amount without including the existing loan or accrued interest. This might lead to incorrect loan accounting.

Overall, the implementation adheres to the required functionality: deposits with user-specific balances, a loan system with dynamic interest calculations, yield distribution, a 50% loan-to-value ratio, a 10% interest rate, and comprehensive error handling. The contract includes both the required functionality and the necessary read-only functions for querying balances and loan amounts.",";; Define the contract's data variables
"""
      }
    ]
)
text = completion.choices[0].message.content.replace('```json', '').replace('```', '')
text = text + "}" if text.endswith('"') else text
print(text)