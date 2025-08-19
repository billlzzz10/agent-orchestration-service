# 🔮 Development Rules & Project Framework

## 📋 Project Overview
**Multi-Agent Orchestration System with Dataset Processing & MCP Integration**

### 🎯 Core Objectives
1. **Dataset Processing Pipeline**: Download, normalize, filter, and cluster instruction datasets
2. **Multi-Agent Orchestration**: Implement flexible agent workflows with 6+ nodes
3. **MCP Integration**: Connect external tools via Model Context Protocol
4. **Quality Evaluation**: Assess dataset and response quality metrics

---

## 🛠 Development Rules

### 1. **Code Quality Standards**
- ✅ **TypeScript/Type Safety**: Use full TypeScript with proper type definitions
- ✅ **Clean Architecture**: Separate interfaces, services, and business logic
- ✅ **Design Patterns**: Implement appropriate patterns (Singleton, Factory, etc.)
- ✅ **Error Handling**: Robust error management with informative logging
- ✅ **Documentation**: Clear comments and README files

### 2. **File Structure Compliance**
```
project/
├── scripts/           # Core processing scripts
├── config/           # Configuration files
├── data/            # Dataset storage
├── tests/           # Test files
├── docs/            # Documentation
└── README files     # Project documentation
```

### 3. **Dependency Management**
- ✅ **Minimal Dependencies**: Use only essential packages
- ✅ **Version Compatibility**: Ensure Python 3.11+ compatibility
- ✅ **Requirements Files**: Maintain updated requirements.txt
- ✅ **Virtual Environments**: Use isolated environments

### 4. **Testing Requirements**
- ✅ **Unit Tests**: Core logic testing
- ✅ **Integration Tests**: Service integration testing
- ✅ **Mock Dependencies**: External API mocking
- ✅ **Error Scenarios**: Edge case testing

---

## 📅 Development Roadmap

### Phase 1: Foundation (Completed ✅)
- [x] Basic dataset processing scripts (1.py, 2.py, 3.py)
- [x] Dataset download automation
- [x] Enhanced filtering and clustering
- [x] Quality evaluation metrics

### Phase 2: Multi-Agent System (Completed ✅)
- [x] Agent orchestrator implementation
- [x] Node-based workflow system
- [x] JSON configuration export
- [x] Tool registry and agent types

### Phase 3: External Integration (Completed ✅)
- [x] Google GenAI Toolbox integration
- [x] Perplexity AI Toolkit integration
- [x] MCP server management
- [x] Enhanced agent capabilities

### Phase 4: Production Readiness (In Progress 🔄)
- [ ] **Performance Optimization**
  - [ ] Async processing for large datasets
  - [ ] Memory-efficient clustering
  - [ ] Caching mechanisms
- [ ] **Scalability Improvements**
  - [ ] Distributed processing support
  - [ ] Load balancing for agents
  - [ ] Database integration
- [ ] **Monitoring & Logging**
  - [ ] Structured logging implementation
  - [ ] Performance metrics collection
  - [ ] Health check endpoints

### Phase 5: Advanced Features (Planned 📋)
- [ ] **Real-time Processing**
  - [ ] Streaming dataset processing
  - [ ] Live agent communication
  - [ ] WebSocket integration
- [ ] **Advanced Analytics**
  - [ ] Dataset quality scoring
  - [ ] Agent performance metrics
  - [ ] Predictive analytics
- [ ] **User Interface**
  - [ ] Web dashboard for monitoring
  - [ ] Configuration management UI
  - [ ] Real-time workflow visualization

---

## 🚀 Current Sprint Goals

### Week 1: Performance & Stability
- [ ] **Optimize build_pairs.py**
  - [ ] Implement async dataset loading
  - [ ] Add progress bars and logging
  - [ ] Memory usage optimization
- [ ] **Enhance MCP System**
  - [ ] Add connection pooling
  - [ ] Implement retry mechanisms
  - [ ] Add health monitoring

### Week 2: Testing & Documentation
- [ ] **Comprehensive Testing**
  - [ ] Unit tests for all core functions
  - [ ] Integration tests for workflows
  - [ ] Performance benchmarks
- [ ] **Documentation Updates**
  - [ ] API documentation
  - [ ] User guides
  - [ ] Deployment instructions

### Week 3: Production Features
- [ ] **Monitoring & Observability**
  - [ ] Structured logging with structlog
  - [ ] Metrics collection with prometheus
  - [ ] Health check endpoints
- [ ] **Configuration Management**
  - [ ] Environment-based configs
  - [ ] Dynamic configuration reloading
  - [ ] Configuration validation

---

## 🔧 Development Workflow

### Before Starting Work
1. **Review Current Status**: Check what's completed and what's next
2. **Plan Implementation**: Break down tasks into manageable chunks
3. **Check Dependencies**: Ensure all required packages are available
4. **Set Up Environment**: Activate correct Python version (3.11+)

### During Development
1. **Follow Code Standards**: Use TypeScript patterns, proper error handling
2. **Test Incrementally**: Test each component as you build
3. **Document Changes**: Update README and comments
4. **Commit Regularly**: Small, focused commits with clear messages

### Before Completion
1. **Run Full Test Suite**: Ensure all tests pass
2. **Performance Check**: Verify no regressions
3. **Documentation Update**: Update relevant documentation
4. **Integration Test**: Test with existing components

---

## 🎯 Quality Gates

### Code Quality
- [ ] **Type Safety**: All functions properly typed
- [ ] **Error Handling**: Comprehensive error management
- [ ] **Documentation**: Clear docstrings and comments
- [ ] **Testing**: >80% code coverage

### Performance
- [ ] **Memory Usage**: Efficient memory utilization
- [ ] **Processing Speed**: Acceptable performance metrics
- [ ] **Scalability**: Handles expected load
- [ ] **Resource Usage**: Optimized CPU/GPU usage

### Integration
- [ ] **API Compatibility**: Works with existing APIs
- [ ] **Data Flow**: Proper data transformation
- [ ] **Error Recovery**: Graceful failure handling
- [ ] **Monitoring**: Observable system behavior

---

## 🚨 Common Issues & Solutions

### Python Version Issues
```bash
# Use Python 3.11 for compatibility
py -3.11 -m pip install -r requirements.txt
py -3.11 scripts/your_script.py
```

### Dependency Conflicts
```bash
# Create fresh virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Memory Issues
- Use streaming datasets for large files
- Implement batch processing
- Add memory monitoring

### Performance Issues
- Profile code with cProfile
- Use async processing where possible
- Implement caching strategies

---

## 📊 Success Metrics

### Technical Metrics
- **Dataset Processing**: >1000 pairs generated successfully
- **Agent Response Time**: <5 seconds for standard queries
- **System Uptime**: >99% availability
- **Error Rate**: <1% failure rate

### Quality Metrics
- **Code Coverage**: >80% test coverage
- **Documentation**: 100% API documented
- **Performance**: No regressions in benchmarks
- **User Satisfaction**: Positive feedback on usability

---

## 🔄 Continuous Improvement

### Weekly Reviews
- Review completed work and challenges
- Update roadmap based on progress
- Identify areas for improvement
- Plan next sprint goals

### Monthly Assessments
- Evaluate overall project progress
- Review technical debt
- Assess team velocity
- Plan major feature releases

---

## 📞 Support & Resources

### Documentation
- `README.md`: Project overview
- `CLAUDE_README.md`: Claude integration guide
- `MCP_README.md`: MCP system documentation
- `INTEGRATED_README.md`: Full system guide

### Key Scripts
- `build_pairs.py`: Main dataset processing
- `agent_orchestrator.py`: Multi-agent system
- `mcp_integrated_system.py`: MCP integration
- `evaluate_dataset.py`: Quality assessment

### Configuration Files
- `requirements_integrated.txt`: All dependencies
- `mcp_config.json`: MCP server configuration
- `agent_flow_config.json`: Agent workflow setup

---

**Remember**: Stay focused on the current phase goals, maintain code quality, and always test thoroughly before moving to the next task! 🚀
