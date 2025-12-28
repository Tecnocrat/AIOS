# 🚀 Quick Start: Testing AIOS Library Ingestion

## 5-Minute Test

Get immediate feedback on Library Ingestion Protocol:

```bash
# 1. Launch workbench
cd c:\dev\AIOS
python testing\library_ingestion_workbench.py

# 2. Select option 8 (Full Integration Test)

# 3. Review results in testing\results\
```

## What This Tests

✅ **Library Ingestion**: Can AIOS parse and understand code?  
✅ **API Discovery**: Does it find functions, classes, methods?  
✅ **Semantic Analysis**: Are tags relevant and meaningful?  
✅ **Search**: Can you find what you learned?  
✅ **Consciousness**: Is quality assessment accurate?

## Expected Results

After running option 8, you should see:

```
🧪 Running Full Integration Test...

Test 1/3: Python json module
✅ Ingestion Complete!
   Duration: ~2-3s
   API Elements: 10-20
   Consciousness: 0.85
   Semantic Tags: 3-5

Test 2/3: API Search
   Found 5+ results

Test 3/3: Report Generation
   Path: testing\results\report_[timestamp].json

✅ Full Integration Test Complete!
```

## Manual Testing Path

For thorough validation:

### Step 1: Test Built-in Library (2 min)
```
Select option: 1
Choose: 1 (json module)
Rate quality: [your rating]
Provide feedback: [your comments]
```

### Step 2: Search APIs (1 min)
```
Select option: 4
Search for: "load"
Verify: Results are relevant
```

### Step 3: View Library Details (1 min)
```
Select option: 5
Select: 1 (json)
Review: API elements, tags, consciousness
```

### Step 4: Generate Report (1 min)
```
Select option: 7
Review: testing\results\report_[session].json
```

## Success Criteria

Your test is successful if:

- ✅ Ingestion completes without errors
- ✅ 10+ API elements discovered
- ✅ Semantic tags are relevant
- ✅ Search finds expected results
- ✅ Report generates successfully

## Common Issues

### "Library ingestion components not available"
**Fix**: Ensure you're running from AIOS root directory

### "Library not found"
**Fix**: Python standard libraries should be auto-detected. If not, use option 2 for custom path.

### Ingestion takes > 10 seconds
**Note**: Large libraries may take longer. This is normal.

## Next Steps

After successful testing:

1. Try option 2 (Custom Library) with your own code
2. Test semantic analysis (option 6) for quality
3. Review generated report for insights
4. Provide feedback for improvements

## Need Help?

- Check `testing/README.md` for detailed documentation
- Review test reports in `testing/results/`
- Check `docs/LIBRARY_INGESTION_PROTOCOL.md` for protocol details

---

**Tip**: Run full integration test (option 8) after any changes to verify nothing broke!
