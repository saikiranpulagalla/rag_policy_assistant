# RAG System Evaluation Results

## Test Questions & Results

### Question 1: "What is the refund window?"
**Expected:** 30 days from purchase
**V1 Answer:** "You can request a refund within 30 days of purchase for most items."
**V2 Answer:** "You can request a refund within 30 days of purchase for most items."
**Result:** ✅ Correct (both versions)
**Notes:** Straightforward factual question, both prompts handle well.

---

### Question 2: "Can I return a digital product?"
**Expected:** No, digital products cannot be refunded once downloaded
**V1 Answer:** "No, digital products or software licenses cannot be refunded once downloaded."
**V2 Answer:** "No, digital products or software licenses cannot be refunded once downloaded."
**Result:** ✅ Correct (both versions)
**Notes:** Clear policy, both versions retrieve and answer correctly.

---

### Question 3: "What's the fastest shipping option?"
**Expected:** Overnight shipping (next business day)
**V1 Answer:** "The fastest shipping option is overnight shipping, which guarantees next business day delivery for $24.99."
**V2 Answer:** "The fastest shipping option is overnight shipping, which guarantees next business day delivery for $24.99."
**Result:** ✅ Correct (both versions)
**Notes:** Explicit in shipping policy, both versions perform well.

---

### Question 4: "Do you offer free returns?"
**Expected:** Not explicitly stated; depends on reason (defective items get free return shipping)
**V1 Answer:** "Return shipping costs are the customer's responsibility unless the item is defective."
**V2 Answer:** "Return shipping costs are the customer's responsibility unless the item is defective. However, if the item is defective, you receive a free return label."
**Result:** ✅ Correct (V2 more complete)
**Notes:** V2 provides more nuanced answer by explicitly stating the exception.

---

### Question 5: "Can I cancel a pre-order?"
**Expected:** Yes, pre-orders can be cancelled anytime before the item ships
**V1 Answer:** "Yes, pre-order items can be cancelled anytime before the item ships."
**V2 Answer:** "Yes, pre-order items can be cancelled anytime before the item ships."
**Result:** ✅ Correct (both versions)
**Notes:** Clear policy statement, both versions retrieve correctly.

---

### Question 6: "What's your return policy for international orders?"
**Expected:** Information not available in documents (shipping policy mentions international shipping, but no specific return policy)
**V1 Answer:** "The documents do not specify a separate return policy for international orders. Standard refund policies apply."
**V2 Answer:** "Information not available in the provided documents. The policy documents cover standard refund procedures but do not specify special handling for international returns."
**Result:** ⚠️ Partially Correct (V2 better)
**Notes:** V2 explicitly uses the fallback phrase, making it clearer that info is missing. V1 makes an inference.

---

### Question 7: "How long does refund processing take?"
**Expected:** 5-7 business days after receiving returned item
**V1 Answer:** "Refunds will be processed within 5-7 business days of receiving the returned item."
**V2 Answer:** "Refunds will be processed within 5-7 business days of receiving the returned item."
**Result:** ✅ Correct (both versions)
**Notes:** Explicit in policy, both versions answer accurately.

---

### Question 8: "Can I return items purchased 60 days ago?"
**Expected:** No, refunds only available within 30 days
**V1 Answer:** "No, items purchased more than 30 days ago cannot be refunded."
**V2 Answer:** "No, items purchased more than 30 days ago cannot be refunded."
**Result:** ✅ Correct (both versions)
**Notes:** Clear policy boundary, both versions handle correctly.

---

## Summary

| Metric | V1 | V2 |
|--------|----|----|
| Correct | 7 | 7 |
| Partially Correct | 1 | 1 |
| Hallucinated | 0 | 0 |
| Accuracy | 87.5% | 87.5% |

## Key Findings

### V1 vs V2 Comparison

**V1 (Basic Prompt):**
- Answers are generally accurate
- Tends to make inferences when information is ambiguous
- Less explicit about information boundaries
- Slightly more prone to filling gaps

**V2 (Improved Prompt):**
- Same accuracy on clear questions
- Better at acknowledging missing information
- More explicit about what's in vs. out of scope
- Uses consistent fallback language
- Better for user trust (clearer about limitations)

### Hallucination Prevention

Both versions performed well on this dataset because:
1. Policy documents are clear and specific
2. Questions are grounded in policy content
3. Retrieval system effectively filters irrelevant chunks

V2 would show more benefit on:
- Ambiguous questions
- Edge cases not covered in policies
- Questions requiring inference

### Recommendations for Production

1. **Use V2 prompt** - Better user experience through explicit boundaries
2. **Increase similarity threshold** - Currently 0.3; consider 0.4+ for stricter filtering
3. **Add question validation** - Reject questions that are too vague
4. **Monitor edge cases** - Track questions that return "Information not available"
5. **Expand policy documents** - Add FAQ section to cover common edge cases

