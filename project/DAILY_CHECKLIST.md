# 📋 Daily Development Checklist

## 🚀 Morning Setup (5 minutes)

### Environment Check
- [ ] **Python Version**: Confirm using Python 3.11+ (`py -3.11 --version`)
- [ ] **Dependencies**: Verify all packages installed (`pip list | grep -E "(datasets|numpy|anthropic|openai)"`)
- [ ] **Working Directory**: Ensure in `project/` folder
- [ ] **Virtual Environment**: Activate if using venv

### Project Status Review
- [ ] **Check Current Phase**: Review `DEVELOPMENT_RULES.md` for current goals
- [ ] **Review TODOs**: Check what's pending from previous session
- [ ] **Check Recent Changes**: Review last few commits or changes
- [ ] **Plan Today's Work**: Identify 2-3 main tasks to focus on

---

## 🔧 Development Session (Work Period)

### Before Starting Code
- [ ] **Task Breakdown**: Break complex tasks into smaller steps
- [ ] **Dependency Check**: Ensure required packages/libraries available
- [ ] **Backup Current State**: Save any important work in progress
- [ ] **Clear Terminal**: Start with clean terminal session

### During Development
- [ ] **Follow Code Standards**: 
  - [ ] Use proper TypeScript patterns
  - [ ] Add error handling
  - [ ] Include docstrings
  - [ ] Follow naming conventions
- [ ] **Test Incrementally**: 
  - [ ] Test each function as you write it
  - [ ] Run existing tests to ensure no regressions
  - [ ] Test edge cases
- [ ] **Document Changes**: 
  - [ ] Update comments in code
  - [ ] Update relevant README files
  - [ ] Note any configuration changes

### Quality Checks (Every 2 hours)
- [ ] **Code Review**: Review your own code for:
  - [ ] Type safety and proper typing
  - [ ] Error handling completeness
  - [ ] Code readability and structure
  - [ ] Performance considerations
- [ ] **Test Run**: 
  - [ ] Run unit tests: `py -3.11 -m pytest tests/`
  - [ ] Run integration tests if applicable
  - [ ] Check for any new errors or warnings
- [ ] **Performance Check**: 
  - [ ] Monitor memory usage for large operations
  - [ ] Check processing time for dataset operations
  - [ ] Verify no memory leaks

---

## 📊 Mid-Session Review (Lunch Break)

### Progress Assessment
- [ ] **Completed Tasks**: Check off what you've finished
- [ ] **Blockers**: Identify any issues preventing progress
- [ ] **Next Steps**: Plan afternoon work
- [ ] **Help Needed**: Note any areas requiring assistance

### System Health Check
- [ ] **Script Functionality**: Test key scripts still work
- [ ] **Data Integrity**: Verify datasets and outputs are correct
- [ ] **Configuration**: Check config files are valid
- [ ] **Dependencies**: Ensure no new dependency issues

---

## 🔍 Afternoon Development

### Focus Areas
- [ ] **Core Features**: Work on main functionality
- [ ] **Testing**: Write/update tests for new features
- [ ] **Documentation**: Update docs for changes
- [ ] **Integration**: Test with other system components

### Quality Assurance
- [ ] **Code Standards**: Ensure all new code meets standards
- [ ] **Error Handling**: Verify comprehensive error management
- [ ] **Performance**: Check for any performance issues
- [ ] **Security**: Review for any security concerns

---

## 📝 End of Day Review (15 minutes)

### Completion Check
- [ ] **Tasks Completed**: Review what was accomplished
- [ ] **Code Committed**: Commit all changes with clear messages
- [ ] **Tests Passing**: Ensure all tests still pass
- [ ] **Documentation Updated**: Verify docs reflect changes

### Next Day Planning
- [ ] **Tomorrow's Goals**: Plan 2-3 main objectives
- [ ] **Blockers Identified**: Note any issues to resolve
- [ ] **Dependencies**: Check if any new packages needed
- [ ] **Priority Setting**: Rank tasks by importance

### System Cleanup
- [ ] **Temporary Files**: Clean up any temp files created
- [ ] **Log Files**: Archive or clean old logs if needed
- [ ] **Cache**: Clear any unnecessary cache files
- [ ] **Environment**: Reset any environment variables if changed

---

## 🚨 Emergency Procedures

### If Scripts Stop Working
1. [ ] **Check Python Version**: Ensure using 3.11+
2. [ ] **Verify Dependencies**: `pip list` to check packages
3. [ ] **Check File Paths**: Ensure working in correct directory
4. [ ] **Review Recent Changes**: What changed before it broke?
5. [ ] **Rollback if Needed**: Revert to last working state

### If Performance Degrades
1. [ ] **Monitor Memory**: Check memory usage
2. [ ] **Profile Code**: Use cProfile to identify bottlenecks
3. [ ] **Check Data Size**: Verify dataset sizes are reasonable
4. [ ] **Review Logs**: Look for error patterns
5. [ ] **Optimize**: Implement fixes for identified issues

### If Integration Fails
1. [ ] **Check API Keys**: Verify all API keys are valid
2. [ ] **Test Connectivity**: Check network connections
3. [ ] **Review Configs**: Verify configuration files
4. [ ] **Check Dependencies**: Ensure all services are running
5. [ ] **Fallback Plan**: Use alternative approaches if needed

---

## 📈 Weekly Review (Friday)

### Progress Assessment
- [ ] **Goals Met**: Review weekly objectives
- [ ] **Code Quality**: Assess overall code quality
- [ ] **Performance**: Check system performance metrics
- [ ] **Documentation**: Verify documentation completeness

### Planning for Next Week
- [ ] **Next Week Goals**: Set objectives for following week
- [ ] **Resource Needs**: Identify any additional resources needed
- [ ] **Training**: Note any skills that need development
- [ ] **Process Improvement**: Identify ways to improve workflow

---

## 🎯 Success Criteria

### Daily Success
- [ ] **Completed Planned Tasks**: At least 80% of planned work done
- [ ] **No Regressions**: All existing functionality still works
- [ ] **Code Quality**: New code meets all standards
- [ ] **Documentation**: Updated for all changes

### Weekly Success
- [ ] **Major Milestones**: Achieved significant progress toward goals
- [ ] **Quality Metrics**: Maintained or improved code quality
- [ ] **Team Collaboration**: Effective communication and coordination
- [ ] **Learning**: Gained new insights or skills

---

## 💡 Tips for Success

### Time Management
- **Pomodoro Technique**: Work in 25-minute focused sessions
- **Priority Matrix**: Focus on high-impact, low-effort tasks first
- **Batch Similar Tasks**: Group related work together
- **Limit Context Switching**: Minimize switching between different types of work

### Quality Focus
- **Test Early, Test Often**: Don't wait until the end to test
- **Code Review**: Review your own code before considering it done
- **Documentation**: Write docs as you code, not after
- **Error Handling**: Always consider what could go wrong

### Continuous Improvement
- **Learn from Mistakes**: Document and learn from errors
- **Seek Feedback**: Ask for input on your approach
- **Stay Updated**: Keep up with best practices and new tools
- **Share Knowledge**: Help others learn from your experiences

---

**Remember**: This checklist is a tool to help you stay organized and productive. Adapt it to your specific needs and workflow! 🚀
