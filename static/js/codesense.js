const { useState, useEffect } = React;

// Lucide Icons as React components
const Upload = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
        <polyline points="17 8 12 3 7 8"></polyline>
        <line x1="12" y1="3" x2="12" y2="15"></line>
    </svg>
);

const Download = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
        <polyline points="7,10 12,15 17,10"/>
        <line x1="12" y1="15" x2="12" y2="3"/>
    </svg>
);

const ChevronDown = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="6,9 12,15 18,9"/>
    </svg>
);

const ChevronUp = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="18,15 12,9 6,15"/>
    </svg>
);

const Shield = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
    </svg>
);

const BarChart = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <line x1="12" y1="20" x2="12" y2="10"/>
        <line x1="18" y1="20" x2="18" y2="4"/>
        <line x1="6" y1="20" x2="6" y2="16"/>
    </svg>
);

const LogOut = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
        <polyline points="16 17 21 12 16 7"></polyline>
        <line x1="21" y1="12" x2="9" y2="12"></line>
    </svg>
);

const User = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
        <circle cx="12" cy="7" r="4"></circle>
    </svg>
);

const AlertCircle = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="8" x2="12" y2="12"></line>
        <line x1="12" y1="16" x2="12.01" y2="16"></line>
    </svg>
);

const CheckCircle = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
        <polyline points="22 4 12 14.01 9 11.01"></polyline>
    </svg>
);

const Info = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="16" x2="12" y2="12"></line>
        <line x1="12" y1="8" x2="12.01" y2="8"></line>
    </svg>
);

const Zap = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
    </svg>
);

const FileText = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
        <polyline points="14 2 14 8 20 8"></polyline>
        <line x1="16" y1="13" x2="8" y2="13"></line>
        <line x1="16" y1="17" x2="8" y2="17"></line>
        <polyline points="10 9 9 9 8 9"></polyline>
    </svg>
);

const Code = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="16 18 22 12 16 6"></polyline>
        <polyline points="8 6 2 12 8 18"></polyline>
    </svg>
);

const LANGUAGES = [
    { value: 'javascript', label: 'JavaScript' },
    { value: 'python', label: 'Python' },
    { value: 'java', label: 'Java' },
    { value: 'cpp', label: 'C++' },
    { value: 'go', label: 'Go' },
];

function CodeSenseAI() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [isSignupMode, setIsSignupMode] = useState(false);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [fullName, setFullName] = useState('');
    const [authError, setAuthError] = useState('');
    const [authLoading, setAuthLoading] = useState(false);
    const [currentUser, setCurrentUser] = useState(null);
    const [showUserMenu, setShowUserMenu] = useState(false);
    const [showSubmissions, setShowSubmissions] = useState(false);
    const [submissions, setSubmissions] = useState([]);
    const [selectedSubmission, setSelectedSubmission] = useState(null);
    const [submissionsLoading, setSubmissionsLoading] = useState(false);
    const [menuTimeout, setMenuTimeout] = useState(null);
    const [collapsedSections, setCollapsedSections] = useState({
        code_output: false,
        output: false,
        issues: false,
        suggestions: false,
        optimizations: false,
        quality: false
    });

    const [code, setCode] = useState('');
    const [language, setLanguage] = useState('javascript');
    const [editor, setEditor] = useState(null);
    const [editorTheme, setEditorTheme] = useState('vs-dark');
    const [uploadedFile, setUploadedFile] = useState(null);
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [analysisResult, setAnalysisResult] = useState(null);

    useEffect(() => {
        const token = localStorage.getItem('codesense_token');
        if (token) {
            // Verify token with backend
            checkAuthStatus(token);
        }
    }, []);

    // Initialize Monaco Editor
    useEffect(() => {
        const initializeEditor = () => {
            require.config({ paths: { vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.44.0/min/vs' } });
            require(['vs/editor/editor.main'], function () {
                const container = document.getElementById('monaco-editor');
                if (!container) return;

                const editorInstance = monaco.editor.create(container, {
                    value: code || '',
                    language: getMonacoLanguage(language),
                    theme: editorTheme,
                    automaticLayout: true,
                    minimap: { enabled: true },
                    fontSize: 14,
                    lineNumbers: 'on',
                    roundedSelection: false,
                    scrollBeyondLastLine: false,
                    readOnly: selectedSubmission !== null,
                    wordWrap: 'on',
                    folding: true,
                    selectOnLineNumbers: true,
                    matchBrackets: 'always',
                    autoIndent: 'full',
                    formatOnPaste: true,
                    formatOnType: true
                });

                editorInstance.onDidChangeModelContent(() => {
                    if (!selectedSubmission) {
                        setCode(editorInstance.getValue());
                    }
                });

                setEditor(editorInstance);
                console.log('Monaco Editor initialized');
                
                setTimeout(() => {
                    editorInstance.layout();
                }, 200);

                return () => {
                    if (editorInstance) {
                        editorInstance.dispose();
                    }
                };
            });
        };

        setTimeout(initializeEditor, 100);
    }, []);

    // Helper function to map language names to Monaco language IDs
    const getMonacoLanguage = (lang) => {
        const languageMap = {
            'javascript': 'javascript',
            'python': 'python',
            'java': 'java',
            'cpp': 'cpp',
            'c': 'c',
            'csharp': 'csharp',
            'typescript': 'typescript',
            'go': 'go',
            'rust': 'rust',
            'php': 'php',
            'ruby': 'ruby',
            'swift': 'swift',
            'kotlin': 'kotlin'
        };
        return languageMap[lang] || 'plaintext';
    };

    // Helper function to clean up code by removing excessive blank lines
    const aggressiveCleanCode = (code) => {
        if (!code) return '';
        
        const normalizedCode = code.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
        const lines = normalizedCode.split('\n');
        const contentLines = [];
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i].trimEnd();
            if (line.trim() !== '') {
                contentLines.push(line);
            }
        }
        
        return contentLines.join('\n');
    };

    // Special effect to handle submission viewing - recreate editor
    useEffect(() => {
        if (selectedSubmission && selectedSubmission.code) {
            const container = document.getElementById('monaco-editor');
            if (!container) return;

            if (editor) {
                editor.dispose();
            }

            require(['vs/editor/editor.main'], function () {
                const cleanedCode = aggressiveCleanCode(selectedSubmission.code);
                
                const newEditor = monaco.editor.create(container, {
                    value: cleanedCode,
                    language: getMonacoLanguage(selectedSubmission.language || language),
                    theme: editorTheme,
                    automaticLayout: true,
                    minimap: { enabled: true },
                    fontSize: 14,
                    lineNumbers: 'on',
                    roundedSelection: false,
                    scrollBeyondLastLine: false,
                    readOnly: true,
                    wordWrap: 'on',
                    folding: true,
                    selectOnLineNumbers: true,
                    matchBrackets: 'always',
                    autoIndent: 'full',
                    formatOnPaste: true,
                    formatOnType: true
                });

                setEditor(newEditor);
                
                setTimeout(() => {
                    newEditor.layout();
                }, 100);
            });
        }
    }, [selectedSubmission]);

    // Update editor theme when theme changes
    useEffect(() => {
        if (editor) {
            monaco.editor.setTheme(editorTheme);
        }
    }, [editorTheme, editor]);

    // Add window resize listener for editor
    useEffect(() => {
        const handleResize = () => {
            if (editor) {
                setTimeout(() => {
                    editor.layout();
                    editor.render(true);
                }, 100);
            }
        };

        window.addEventListener('resize', handleResize);
        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, [editor]);

    // Cleanup timeout on unmount
    useEffect(() => {
        return () => {
            if (menuTimeout) {
                clearTimeout(menuTimeout);
            }
        };
    }, [menuTimeout]);

    // Update editor language when language changes
    useEffect(() => {
        if (editor && !selectedSubmission) {
            const model = editor.getModel();
            if (model) {
                monaco.editor.setModelLanguage(model, getMonacoLanguage(language));
            }
        }
    }, [language, editor, selectedSubmission]);

    const checkAuthStatus = async (token) => {
        try {
            const response = await fetch('/auth/me', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            if (response.ok) {
                const userData = await response.json();
                setCurrentUser(userData);
                setUsername(userData.username);
                setIsLoggedIn(true);
            } else {
                localStorage.removeItem('codesense_token');
            }
        } catch (error) {
            localStorage.removeItem('codesense_token');
        }
    };

    const handleAuth = async (e) => {
        e.preventDefault();
        setAuthError('');
        setAuthLoading(true);
        
        // Validate password length for bcrypt compatibility
        if (password.length > 72) {
            setAuthError('Password is too long. Please use 72 characters or fewer.');
            setAuthLoading(false);
            return;
        }
        
        const endpoint = isSignupMode ? '/auth/signup' : '/auth/login';
        const payload = isSignupMode 
            ? { username, password, email: email || null, full_name: fullName || null }
            : { username, password };
        
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            
            const data = await response.json();
            
            if (response.ok) {
                localStorage.setItem('codesense_token', data.access_token);
                setCurrentUser(data.user);
                setUsername(data.user.username);
                setIsLoggedIn(true);
                // Clear form
                setPassword('');
                setEmail('');
                setFullName('');
            } else {
                setAuthError(data.detail || 'Authentication failed');
            }
        } catch (error) {
            setAuthError('Connection error. Please try again.');
        } finally {
            setAuthLoading(false);
        }
    };

    const handleLogout = async () => {
        try {
            const token = localStorage.getItem('codesense_token');
            if (token) {
                await fetch('/auth/logout', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
            }
        } catch (error) {
            console.log('Logout request failed, but continuing...');
        }
        
        localStorage.removeItem('codesense_token');
        setIsLoggedIn(false);
        setCurrentUser(null);
        setUsername('');
        setCode('');
        setUploadedFile(null);
        setAnalysisResult(null);
        setShowSubmissions(false);
        setSubmissions([]);
        setSelectedSubmission(null);
    };

    const fetchSubmissions = async () => {
        setSubmissionsLoading(true);
        try {
            const token = localStorage.getItem('codesense_token');
            const response = await fetch('/api/submissions', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setSubmissions(data.submissions || []);
            } else {
                console.error('Failed to fetch submissions');
            }
        } catch (error) {
            console.error('Error fetching submissions:', error);
        } finally {
            setSubmissionsLoading(false);
        }
    };

    const fetchSubmission = async (submissionId) => {
        try {
            const token = localStorage.getItem('codesense_token');
            const response = await fetch(`/api/submissions/${submissionId}`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (response.ok) {
                const submission = await response.json();
                setSelectedSubmission(submission);
                setCode(submission.code);
                setLanguage(submission.language);
                setAnalysisResult(submission.analysis_result);
                setUploadedFile(submission.file_name);
                setShowSubmissions(false);
            } else {
                console.error('Failed to fetch submission');
            }
        } catch (error) {
            console.error('Error fetching submission:', error);
        }
    };

    const handleShowSubmissions = () => {
        setShowSubmissions(true);
        setSelectedSubmission(null);
        fetchSubmissions();
    };

    const handleBackToEditor = () => {
        setShowSubmissions(false);
        setSelectedSubmission(null);
        setCode('');
        setAnalysisResult(null);
        setUploadedFile(null);
        
        // Recreate editor for normal editing
        const container = document.getElementById('monaco-editor');
        if (container && editor) {
            editor.dispose();
            
            require(['vs/editor/editor.main'], function () {
                const newEditor = monaco.editor.create(container, {
                    value: '',
                    language: getMonacoLanguage(language),
                    theme: editorTheme,
                    automaticLayout: true,
                    minimap: { enabled: true },
                    fontSize: 14,
                    lineNumbers: 'on',
                    roundedSelection: false,
                    scrollBeyondLastLine: false,
                    readOnly: false,
                    wordWrap: 'on',
                    folding: true,
                    selectOnLineNumbers: true,
                    matchBrackets: 'always',
                    autoIndent: 'full',
                    formatOnPaste: true,
                    formatOnType: true
                });

                newEditor.onDidChangeModelContent(() => {
                    setCode(newEditor.getValue());
                });

                setEditor(newEditor);
            });
        }
    };

    const handleMenuEnter = () => {
        if (menuTimeout) {
            clearTimeout(menuTimeout);
            setMenuTimeout(null);
        }
        setShowUserMenu(true);
    };

    const handleMenuLeave = () => {
        const timeout = setTimeout(() => {
            setShowUserMenu(false);
        }, 150); // 150ms delay
        setMenuTimeout(timeout);
    };

    const toggleSection = (section) => {
        setCollapsedSections(prev => ({
            ...prev,
            [section]: !prev[section]
        }));
    };

    const handleFileUpload = (e) => {
        const file = e.target.files?.[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (event) => {
            const content = event.target?.result;
            setCode(content);
            setUploadedFile(file.name);
            
            const ext = file.name.split('.').pop()?.toLowerCase();
            const langMap = {
                'js': 'javascript', 'jsx': 'javascript',
                'py': 'python',
                'java': 'java',
                'cpp': 'cpp', 'cc': 'cpp', 'cxx': 'cpp', 'c': 'cpp', 'h': 'cpp', 'hpp': 'cpp',
                'go': 'go',
            };
            if (ext && langMap[ext]) {
                setLanguage(langMap[ext]);
            }
        };
        reader.readAsText(file);
    };

    const handleAnalyze = async () => {
        if (!code.trim()) {
            alert('Please enter or upload some code to analyze');
            return;
        }

        setIsAnalyzing(true);
        setAnalysisResult(null);

        try {
            const token = localStorage.getItem('codesense_token');
            if (!token) {
                alert('Please log in to analyze code');
                return;
            }
            
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ code: code, language: language }),
            });

            const data = await response.json();
            
            if (response.ok) {
                setAnalysisResult(data);
            } else if (response.status === 401 || response.status === 403) {
                // Token expired or invalid - redirect to login
                localStorage.removeItem('codesense_token');
                setIsLoggedIn(false);
                setCurrentUser(null);
                alert('Your session has expired. Please log in again.');
            } else {
                setAnalysisResult({
                    errors: [{ line: 1, message: data.detail || 'Analysis failed', severity: 'error' }],
                    suggestions: [],
                    optimizations: [],
                    output: 'Analysis failed',
                });
            }
        } catch (error) {
            setAnalysisResult({
                errors: [{ line: 1, message: 'Failed to connect to analysis service', severity: 'error' }],
                suggestions: [],
                optimizations: [],
                output: 'Connection error',
            });
        } finally {
            setIsAnalyzing(false);
        }
    };

    const handleDownloadReport = () => {
        if (!analysisResult) return;

        let reportContent = '=== CodeSense AI Analysis Report ===\n\n';
        
        if (selectedSubmission) {
            reportContent += `Generated: ${new Date(selectedSubmission.created_at).toLocaleString()}\n`;
            reportContent += `Retrieved: ${new Date().toLocaleString()}\n`;
            reportContent += `User: ${username}\n`;
            reportContent += `Language: ${selectedSubmission.language}\n`;
            reportContent += `File: ${selectedSubmission.file_name}\n\n`;
        } else {
            reportContent += `Generated: ${new Date().toLocaleString()}\n`;
            reportContent += `User: ${username}\n`;
            reportContent += `Language: ${language}\n`;
            
            if (uploadedFile) {
                reportContent += `File: ${uploadedFile}\n\n`;
            } else {
                reportContent += '\n--- Code ---\n';
                reportContent += code + '\n\n';
            }
        }

        // Add Quality Metrics section (now first)
        if (analysisResult.quality_metrics) {
            reportContent += '--- Code Quality Metrics ---\n';
            reportContent += `Summary: ${analysisResult.quality_metrics.summary}\n`;
            reportContent += `Overall Score: ${analysisResult.quality_metrics.overall_score}/100\n`;
            reportContent += `Cyclomatic Complexity: ${analysisResult.quality_metrics.cyclomatic_complexity}\n`;
            reportContent += `Lines of Code: ${analysisResult.quality_metrics.lines_of_code}\n`;
            reportContent += `Time Complexity: ${analysisResult.quality_metrics.time_complexity}\n`;
            reportContent += `Space Complexity: ${analysisResult.quality_metrics.space_complexity}\n`;
            if (analysisResult.quality_metrics.security_analysis) {
                reportContent += `Security Analysis: ${analysisResult.quality_metrics.security_analysis}\n`;
            }
            
            if (analysisResult.quality_metrics.complexity_issues && analysisResult.quality_metrics.complexity_issues.length > 0) {
                reportContent += '\nComplexity Issues:\n';
                analysisResult.quality_metrics.complexity_issues.forEach((issue, idx) => {
                    reportContent += `${idx + 1}. ${issue}\n`;
                });
            }
            
            if (analysisResult.quality_metrics.security_issues && analysisResult.quality_metrics.security_issues.length > 0) {
                reportContent += '\nSecurity Issues:\n';
                analysisResult.quality_metrics.security_issues.forEach((issue, idx) => {
                    reportContent += `${idx + 1}. ${issue}\n`;
                });
            }
            
            if (analysisResult.quality_metrics.recommendations && analysisResult.quality_metrics.recommendations.length > 0) {
                reportContent += '\nQuality Recommendations:\n';
                analysisResult.quality_metrics.recommendations.forEach((rec, idx) => {
                    reportContent += `${idx + 1}. ${rec}\n`;
                });
            }
            reportContent += '\n';
        }

        reportContent += '--- Code Output ---\n';
        reportContent += analysisResult.output || 'No output detected';
        reportContent += '\n\n';

        reportContent += '--- Issues Found ---\n';
        if (analysisResult.errors && analysisResult.errors.length > 0) {
            analysisResult.errors.forEach((error, idx) => {
                reportContent += `${idx + 1}. [${error.severity.toUpperCase()}] Line ${error.line}: ${error.message}\n`;
            });
        } else {
            reportContent += 'No issues found\n';
        }
        reportContent += '\n';

        reportContent += '--- Suggestions ---\n';
        if (analysisResult.suggestions && analysisResult.suggestions.length > 0) {
            analysisResult.suggestions.forEach((suggestion, idx) => {
                reportContent += `${idx + 1}. ${suggestion}\n`;
            });
        } else {
            reportContent += 'No suggestions available\n';
        }
        reportContent += '\n';

        reportContent += '--- Optimizations ---\n';
        if (analysisResult.optimizations && analysisResult.optimizations.length > 0) {
            analysisResult.optimizations.forEach((optimization, idx) => {
                reportContent += `${idx + 1}. ${optimization}\n`;
            });
        } else {
            reportContent += 'No optimizations suggested\n';
        }

        const blob = new Blob([reportContent], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `codesense-report-${Date.now()}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    if (!isLoggedIn) {
        return (
            <div 
                className="min-h-screen flex items-center justify-end p-8 relative"
                style={{
                    backgroundImage: 'url(/static/images/workspace-hero.jpg)',
                    backgroundSize: 'cover',
                    backgroundPosition: 'center',
                    backgroundRepeat: 'no-repeat'
                }}
            >
                {/* Floating Login Panel */}
                <div className="login-panel rounded-3xl shadow-2xl p-8 w-full max-w-md mr-16">
                    <div className="text-center mb-8">
                        <div className="inline-flex items-center justify-center w-16 h-16 bg-amber-800 rounded-full mb-4">
                            <Code />
                        </div>
                        <h1 className="text-3xl font-bold text-gray-900 mb-2">CodeSense AI</h1>
                        <p className="text-gray-600">{isSignupMode ? 'Create your account' : 'Sign in to analyze your code'}</p>
                    </div>

                    <div className="flex mb-6 bg-gray-100 rounded-lg p-1">
                        <button
                            onClick={() => { setIsSignupMode(false); setAuthError(''); }}
                            className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                                !isSignupMode 
                                    ? 'bg-white text-indigo-600 shadow-sm' 
                                    : 'text-gray-600 hover:text-gray-900'
                            }`}
                        >
                            Login
                        </button>
                        <button
                            onClick={() => { setIsSignupMode(true); setAuthError(''); }}
                            className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                                isSignupMode 
                                    ? 'bg-white text-indigo-600 shadow-sm' 
                                    : 'text-gray-600 hover:text-gray-900'
                            }`}
                        >
                            Sign Up
                        </button>
                    </div>

                    <form onSubmit={handleAuth} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Username</label>
                            <input
                                type="text"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                                placeholder="Enter your username"
                                required
                                disabled={authLoading}
                            />
                        </div>

                        {isSignupMode && (
                            <>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">Email (Optional)</label>
                                    <input
                                        type="email"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                                        placeholder="Enter your email"
                                        disabled={authLoading}
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">Full Name (Optional)</label>
                                    <input
                                        type="text"
                                        value={fullName}
                                        onChange={(e) => setFullName(e.target.value)}
                                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                                        placeholder="Enter your full name"
                                        disabled={authLoading}
                                    />
                                </div>
                            </>
                        )}

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Password</label>
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                                placeholder={isSignupMode ? 'Create a password (6-72 chars)' : 'Enter your password'}
                                required
                                disabled={authLoading}
                                maxLength={72}
                            />
                        </div>

                        {authError && (
                            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
                                {authError}
                            </div>
                        )}

                        <button
                            type="submit"
                            disabled={authLoading || !username.trim() || !password.trim()}
                            className="w-full bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center justify-center space-x-2"
                        >
                            {authLoading ? (
                                <>
                                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                                    <span>{isSignupMode ? 'Creating Account...' : 'Signing In...'}</span>
                                </>
                            ) : (
                                <span>{isSignupMode ? 'Create Account' : 'Sign In'}</span>
                            )}
                        </button>
                    </form>

                    <p className="text-center text-sm text-gray-600 mt-4">
                        {isSignupMode 
                            ? 'Already have an account? Click Login above' 
                            : 'New user? Click Sign Up above to create an account'
                        }
                    </p>
                </div>
            </div>
        );

    }

    return (
        <div className="min-h-screen bg-gray-50">
            <header className="bg-white shadow-sm border-b border-gray-200">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <div className="flex justify-between items-center">
                        <div className="flex items-center space-x-3">
                            <div className="bg-indigo-600 p-2 rounded-lg">
                                <Code />
                            </div>
                            <div>
                                <h1 className="text-2xl font-bold text-gray-900">CodeSense AI</h1>
                                <p className="text-sm text-gray-600">AI-Powered Code Analysis</p>
                            </div>
                        </div>
                        
                        <div className="flex items-center space-x-4">
                            <div className="relative">
                                <div 
                                    className="flex items-center space-x-2 px-4 py-2 bg-gray-100 rounded-lg cursor-pointer hover:bg-gray-200 transition-colors"
                                    onMouseEnter={handleMenuEnter}
                                    onMouseLeave={handleMenuLeave}
                                >
                                    <User />
                                    <span className="text-sm font-medium text-gray-700">
                                        {currentUser?.full_name || username}
                                    </span>
                                </div>
                                
                                {showUserMenu && (
                                    <div 
                                        className="absolute right-0 mt-1 w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-50"
                                        onMouseEnter={handleMenuEnter}
                                        onMouseLeave={handleMenuLeave}
                                    >
                                        <button
                                            onClick={handleShowSubmissions}
                                            className="w-full text-left px-4 py-3 text-sm text-gray-700 hover:bg-gray-50 flex items-center space-x-2"
                                        >
                                            <FileText />
                                            <span>Past Submissions</span>
                                        </button>
                                        <hr className="border-gray-200" />
                                        <button
                                            onClick={handleLogout}
                                            className="w-full text-left px-4 py-3 text-sm text-red-600 hover:bg-red-50 flex items-center space-x-2"
                                        >
                                            <LogOut />
                                            <span>Logout</span>
                                        </button>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </header>

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {showSubmissions ? (
                    <div className="space-y-6">
                        <div className="flex items-center justify-between">
                            <h2 className="text-2xl font-bold text-gray-900">Past Submissions</h2>
                            <button
                                onClick={handleBackToEditor}
                                className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
                            >
                                <span>← Back to Editor</span>
                            </button>
                        </div>
                        
                        {submissionsLoading ? (
                            <div className="flex justify-center py-12">
                                <div className="w-8 h-8 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin" />
                            </div>
                        ) : submissions.length === 0 ? (
                            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
                                <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                                <h3 className="text-lg font-semibold text-gray-900 mb-2">No Submissions Yet</h3>
                                <p className="text-gray-600">Start analyzing code to see your submission history here.</p>
                            </div>
                        ) : (
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                {submissions.map((submission) => (
                                    <div 
                                        key={submission.id}
                                        className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow cursor-pointer"
                                        onClick={() => fetchSubmission(submission.id)}
                                    >
                                        <div className="flex items-center space-x-3 mb-4">
                                            <div className="bg-indigo-100 p-2 rounded-lg">
                                                <Code className="w-5 h-5 text-indigo-600" />
                                            </div>
                                            <div>
                                                <h3 className="font-semibold text-gray-900">{submission.file_name}</h3>
                                                <p className="text-sm text-gray-600 capitalize">{submission.language}</p>
                                            </div>
                                        </div>
                                        <p className="text-sm text-gray-500">
                                            {new Date(submission.created_at).toLocaleString()}
                                        </p>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                ) : (
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <div className="space-y-6">
                        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                            <h2 className="text-xl font-semibold text-gray-900 mb-4">
                                {selectedSubmission ? 'Past Submission' : 'Code Input'}
                            </h2>
                            
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">Programming Language</label>
                                    <select
                                        value={language}
                                        onChange={(e) => setLanguage(e.target.value)}
                                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                                        disabled={selectedSubmission !== null}
                                    >
                                        {LANGUAGES.map((lang) => (
                                            <option key={lang.value} value={lang.value}>{lang.label}</option>
                                        ))}
                                    </select>
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">Editor Theme</label>
                                    <select
                                        value={editorTheme}
                                        onChange={(e) => setEditorTheme(e.target.value)}
                                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                                        disabled={selectedSubmission !== null}
                                    >
                                        <option value="vs-dark">Dark (VS Code)</option>
                                        <option value="vs">Light</option>
                                        <option value="hc-black">High Contrast Dark</option>
                                        <option value="hc-light">High Contrast Light</option>
                                    </select>
                                </div>
                            </div>

                            {!selectedSubmission && (
                                <div className="mb-4">
                                    <label className="block text-sm font-medium text-gray-700 mb-2">Upload File</label>
                                    <div className="relative">
                                        <input
                                            type="file"
                                            onChange={handleFileUpload}
                                            className="hidden"
                                            id="file-upload"
                                            accept=".js,.jsx,.py,.java,.cpp,.cc,.cxx,.c,.h,.hpp,.go"
                                        />
                                        <label
                                            htmlFor="file-upload"
                                            className="flex items-center justify-center space-x-2 w-full px-4 py-3 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:border-indigo-500 hover:bg-indigo-50 transition-colors"
                                        >
                                            <Upload />
                                            <span className="text-sm text-gray-600">
                                                {uploadedFile || 'Click to upload code file'}
                                            </span>
                                        </label>
                                    </div>
                                </div>
                            )}

                            <div className="mb-4">
                                <div className="flex items-center justify-between mb-2">
                                    <label className="block text-sm font-medium text-gray-700">
                                        {selectedSubmission ? 'Code (Read-only)' : 'Code Editor'}
                                    </label>
                                    {selectedSubmission && (
                                        <span className="text-xs text-blue-600 bg-blue-50 px-2 py-1 rounded-full">
                                            Viewing Past Submission
                                        </span>
                                    )}
                                </div>
                                <div
                                    id="monaco-editor"
                                    className={`w-full border rounded-lg ${
                                        selectedSubmission 
                                            ? 'border-gray-200 bg-gray-50' 
                                            : 'border-gray-300'
                                    }`}
                                    style={{ height: '400px', minHeight: '400px' }}
                                ></div>
                            </div>

                            {!selectedSubmission && (
                                <button
                                    onClick={handleAnalyze}
                                    disabled={isAnalyzing || !code.trim()}
                                    className="w-full bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center justify-center space-x-2"
                                >
                                    {isAnalyzing ? (
                                        <>
                                            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                                            <span>Analyzing...</span>
                                        </>
                                    ) : (
                                        <>
                                            <Zap />
                                            <span>Analyze Code</span>
                                        </>
                                    )}
                                </button>
                            )}

                            {selectedSubmission && (
                                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                                    <div className="flex items-center space-x-2 text-blue-700">
                                        <FileText className="w-5 h-5" />
                                        <span className="font-medium">Past Submission</span>
                                    </div>
                                    <p className="text-sm text-blue-600 mt-1">
                                        Submitted on {new Date(selectedSubmission.created_at).toLocaleString()}
                                    </p>
                                    <button
                                        onClick={handleBackToEditor}
                                        className="mt-3 px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition-colors"
                                    >
                                        ← Back to Editor
                                    </button>
                                </div>
                            )}
                        </div>
                    </div>

                    <div className="space-y-6">
                        {analysisResult ? (
                            <>
                                <button
                                    onClick={handleDownloadReport}
                                    className="w-full bg-green-600 text-white py-3 rounded-lg font-semibold hover:bg-green-700 transition-colors flex items-center justify-center space-x-2"
                                >
                                    <Download />
                                    <span>Download Report</span>
                                </button>

                                {/* Quality Metrics - Collapsible */}
                                <div className="bg-white rounded-xl shadow-sm border border-gray-200">
                                    <button
                                        onClick={() => toggleSection('quality')}
                                        className="w-full p-6 text-left flex items-center justify-between hover:bg-gray-50 transition-colors"
                                    >
                                        <div className="flex items-center space-x-2">
                                            <BarChart />
                                            <span className="text-lg font-semibold text-gray-900">Code Quality Metrics</span>
                                            {analysisResult.quality_metrics && analysisResult.quality_metrics.overall_score && (
                                                <span className={`text-xs px-2 py-1 rounded-full ${
                                                    analysisResult.quality_metrics.overall_score >= 80 
                                                        ? 'bg-green-100 text-green-800'
                                                        : analysisResult.quality_metrics.overall_score >= 60
                                                        ? 'bg-yellow-100 text-yellow-800'
                                                        : 'bg-red-100 text-red-800'
                                                }`}>
                                                    {analysisResult.quality_metrics.overall_score}/100
                                                </span>
                                            )}
                                        </div>
                                        {collapsedSections.quality ? <ChevronDown /> : <ChevronUp />}
                                    </button>
                                    {!collapsedSections.quality && analysisResult.quality_metrics && (
                                        <div className="px-6 pb-6 space-y-4">
                                            {/* Summary */}
                                            <div className="bg-gray-50 rounded-lg p-4">
                                                <h4 className="font-semibold text-sm text-gray-900 mb-2">Summary</h4>
                                                <p className="text-sm text-gray-700">{analysisResult.quality_metrics.summary}</p>
                                            </div>

                                            {/* Overall Score */}
                                            <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-4 text-center">
                                                <h4 className="font-semibold text-lg text-gray-900 mb-2">Overall Code Quality Score</h4>
                                                <div className={`text-4xl font-bold mb-2 ${
                                                    analysisResult.quality_metrics.overall_score >= 80 
                                                        ? 'text-green-600'
                                                        : analysisResult.quality_metrics.overall_score >= 60
                                                        ? 'text-yellow-600'
                                                        : 'text-red-600'
                                                }`}>
                                                    {analysisResult.quality_metrics.overall_score}/100
                                                </div>
                                                <p className="text-sm text-gray-600">
                                                    {analysisResult.quality_metrics.overall_score >= 80 
                                                        ? 'Excellent code quality'
                                                        : analysisResult.quality_metrics.overall_score >= 60
                                                        ? 'Good code quality'
                                                        : 'Needs improvement'}
                                                </p>
                                            </div>

                                            {/* Metrics Grid */}
                                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                                <div className="bg-orange-50 rounded-lg p-4">
                                                    <h4 className="font-semibold text-sm text-orange-900 mb-1">Cyclomatic Complexity</h4>
                                                    <p className="text-sm text-orange-700">{analysisResult.quality_metrics.cyclomatic_complexity}</p>
                                                </div>
                                                <div className="bg-blue-50 rounded-lg p-4">
                                                    <h4 className="font-semibold text-sm text-blue-900 mb-1">Lines of Code</h4>
                                                    <p className="text-sm text-blue-700">{analysisResult.quality_metrics.lines_of_code}</p>
                                                </div>
                                                <div className="bg-purple-50 rounded-lg p-4">
                                                    <h4 className="font-semibold text-sm text-purple-900 mb-1">Time Complexity</h4>
                                                    <p className="text-sm text-purple-700">{analysisResult.quality_metrics.time_complexity}</p>
                                                </div>
                                                <div className="bg-teal-50 rounded-lg p-4">
                                                    <h4 className="font-semibold text-sm text-teal-900 mb-1">Space Complexity</h4>
                                                    <p className="text-sm text-teal-700">{analysisResult.quality_metrics.space_complexity}</p>
                                                </div>
                                            </div>

                                            {/* Security Analysis */}
                                            {analysisResult.quality_metrics.security_analysis && (
                                                <div className="bg-red-50 rounded-lg p-4">
                                                    <div className="flex items-center space-x-2 mb-2">
                                                        <Shield />
                                                        <h4 className="font-semibold text-sm text-red-900">Security Analysis</h4>
                                                    </div>
                                                    <p className="text-sm text-red-700">{analysisResult.quality_metrics.security_analysis}</p>
                                                </div>
                                            )}

                                            {/* Issues Lists */}
                                            {analysisResult.quality_metrics.complexity_issues && analysisResult.quality_metrics.complexity_issues.length > 0 && (
                                                <div>
                                                    <h4 className="font-semibold text-sm text-gray-900 mb-2">Complexity Issues</h4>
                                                    <ul className="space-y-1">
                                                        {analysisResult.quality_metrics.complexity_issues.map((issue, idx) => (
                                                            <li key={idx} className="flex items-start space-x-2 text-sm text-gray-700">
                                                                <span className="text-orange-600 font-bold">•</span>
                                                                <span>{issue}</span>
                                                            </li>
                                                        ))}
                                                    </ul>
                                                </div>
                                            )}

                                            {analysisResult.quality_metrics.security_issues && analysisResult.quality_metrics.security_issues.length > 0 && (
                                                <div>
                                                    <h4 className="font-semibold text-sm text-gray-900 mb-2">Security Issues</h4>
                                                    <ul className="space-y-1">
                                                        {analysisResult.quality_metrics.security_issues.map((issue, idx) => (
                                                            <li key={idx} className="flex items-start space-x-2 text-sm text-gray-700">
                                                                <span className="text-red-600 font-bold">•</span>
                                                                <span>{issue}</span>
                                                            </li>
                                                        ))}
                                                    </ul>
                                                </div>
                                            )}

                                            {/* Recommendations */}
                                            {analysisResult.quality_metrics.recommendations && analysisResult.quality_metrics.recommendations.length > 0 && (
                                                <div>
                                                    <h4 className="font-semibold text-sm text-gray-900 mb-2">Recommendations</h4>
                                                    <ul className="space-y-1">
                                                        {analysisResult.quality_metrics.recommendations.map((rec, idx) => (
                                                            <li key={idx} className="flex items-start space-x-2 text-sm text-gray-700">
                                                                <span className="text-green-600 font-bold">•</span>
                                                                <span>{rec}</span>
                                                            </li>
                                                        ))}
                                                    </ul>
                                                </div>
                                            )}
                                        </div>
                                    )}
                                </div>

                                {/* Issues Found - Collapsible */}
                                <div className="bg-white rounded-xl shadow-sm border border-gray-200">
                                    <button
                                        onClick={() => toggleSection('issues')}
                                        className="w-full p-6 text-left flex items-center justify-between hover:bg-gray-50 transition-colors"
                                    >
                                        <div className="flex items-center space-x-2">
                                            <AlertCircle />
                                            <span className="text-lg font-semibold text-gray-900">Issues Found</span>
                                            {analysisResult.errors && analysisResult.errors.length > 0 && (
                                                <span className="bg-red-100 text-red-800 text-xs px-2 py-1 rounded-full">
                                                    {analysisResult.errors.length}
                                                </span>
                                            )}
                                        </div>
                                        {collapsedSections.issues ? <ChevronDown /> : <ChevronUp />}
                                    </button>
                                    {!collapsedSections.issues && (
                                        <div className="px-6 pb-6">
                                            {analysisResult.errors && analysisResult.errors.length > 0 ? (
                                                <div className="space-y-2">
                                                    {analysisResult.errors.map((error, idx) => (
                                                        <div
                                                            key={idx}
                                                            className={`p-3 rounded-lg border ${
                                                                error.severity === 'error'
                                                                    ? 'bg-red-50 border-red-200'
                                                                    : error.severity === 'warning'
                                                                    ? 'bg-yellow-50 border-yellow-200'
                                                                    : 'bg-blue-50 border-blue-200'
                                                            }`}
                                                        >
                                                            <div className="flex items-start space-x-2">
                                                                <span className="font-semibold text-sm">Line {error.line}:</span>
                                                                <span className="text-sm">{error.message}</span>
                                                            </div>
                                                        </div>
                                                    ))}
                                                </div>
                                            ) : (
                                                <p className="text-green-600 text-sm">No issues found! Your code looks good.</p>
                                            )}
                                        </div>
                                    )}
                                </div>

                                {/* Suggestions - Collapsible */}
                                <div className="bg-white rounded-xl shadow-sm border border-gray-200">
                                    <button
                                        onClick={() => toggleSection('suggestions')}
                                        className="w-full p-6 text-left flex items-center justify-between hover:bg-gray-50 transition-colors"
                                    >
                                        <div className="flex items-center space-x-2">
                                            <Info />
                                            <span className="text-lg font-semibold text-gray-900">Suggestions</span>
                                            {analysisResult.suggestions && analysisResult.suggestions.length > 0 && (
                                                <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
                                                    {analysisResult.suggestions.length}
                                                </span>
                                            )}
                                        </div>
                                        {collapsedSections.suggestions ? <ChevronDown /> : <ChevronUp />}
                                    </button>
                                    {!collapsedSections.suggestions && (
                                        <div className="px-6 pb-6">
                                            {analysisResult.suggestions && analysisResult.suggestions.length > 0 ? (
                                                <ul className="space-y-2">
                                                    {analysisResult.suggestions.map((suggestion, idx) => (
                                                        <li key={idx} className="flex items-start space-x-2 text-sm text-gray-700">
                                                            <span className="text-blue-600 font-bold">•</span>
                                                            <span>{suggestion}</span>
                                                        </li>
                                                    ))}
                                                </ul>
                                            ) : (
                                                <p className="text-gray-600 text-sm">No suggestions available</p>
                                            )}
                                        </div>
                                    )}
                                </div>

                                {/* Optimizations - Collapsible */}
                                <div className="bg-white rounded-xl shadow-sm border border-gray-200">
                                    <button
                                        onClick={() => toggleSection('optimizations')}
                                        className="w-full p-6 text-left flex items-center justify-between hover:bg-gray-50 transition-colors"
                                    >
                                        <div className="flex items-center space-x-2">
                                            <CheckCircle />
                                            <span className="text-lg font-semibold text-gray-900">Optimizations</span>
                                            {analysisResult.optimizations && analysisResult.optimizations.length > 0 && (
                                                <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">
                                                    {analysisResult.optimizations.length}
                                                </span>
                                            )}
                                        </div>
                                        {collapsedSections.optimizations ? <ChevronDown /> : <ChevronUp />}
                                    </button>
                                    {!collapsedSections.optimizations && (
                                        <div className="px-6 pb-6">
                                            {analysisResult.optimizations && analysisResult.optimizations.length > 0 ? (
                                                <ul className="space-y-2">
                                                    {analysisResult.optimizations.map((optimization, idx) => (
                                                        <li key={idx} className="flex items-start space-x-2 text-sm text-gray-700">
                                                            <span className="text-green-600 font-bold">•</span>
                                                            <span>{optimization}</span>
                                                        </li>
                                                    ))}
                                                </ul>
                                            ) : (
                                                <p className="text-gray-600 text-sm">No optimizations suggested</p>
                                            )}
                                        </div>
                                    )}
                                </div>

                                {/* Actual Code Execution Output - Collapsible */}
                                <div className="bg-white rounded-xl shadow-sm border border-gray-200">
                                    <button
                                        onClick={() => toggleSection('code_output')}
                                        className="w-full p-6 text-left flex items-center justify-between hover:bg-gray-50 transition-colors"
                                    >
                                        <div className="flex items-center space-x-2">
                                            <Code />
                                            <span className="text-lg font-semibold text-gray-900">Code Execution Output</span>
                                            {analysisResult.execution_success ? (
                                                <span className="ml-2 px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">Success</span>
                                            ) : (
                                                <span className="ml-2 px-2 py-1 text-xs font-medium bg-red-100 text-red-800 rounded-full">Failed</span>
                                            )}
                                        </div>
                                        {collapsedSections.code_output ? <ChevronDown /> : <ChevronUp />}
                                    </button>
                                    {!collapsedSections.code_output && (
                                        <div className="px-6 pb-6">
                                            <div className={`rounded-lg p-4 font-mono text-sm whitespace-pre-wrap ${
                                                analysisResult.execution_success 
                                                    ? 'bg-green-50 text-green-800 border border-green-200' 
                                                    : 'bg-red-50 text-red-800 border border-red-200'
                                            }`}>
                                                {analysisResult.code_output || "No execution output"}
                                            </div>
                                        </div>
                                    )}
                                </div>

                                {/* AI Analysis Output - Collapsible */}
                                <div className="bg-white rounded-xl shadow-sm border border-gray-200">
                                    <button
                                        onClick={() => toggleSection('output')}
                                        className="w-full p-6 text-left flex items-center justify-between hover:bg-gray-50 transition-colors"
                                    >
                                        <div className="flex items-center space-x-2">
                                            <FileText />
                                            <span className="text-lg font-semibold text-gray-900">AI Analysis</span>
                                        </div>
                                        {collapsedSections.output ? <ChevronDown /> : <ChevronUp />}
                                    </button>
                                    {!collapsedSections.output && (
                                        <div className="px-6 pb-6">
                                            <div className="bg-gray-50 rounded-lg p-4 font-mono text-sm text-gray-800 whitespace-pre-wrap">
                                                {analysisResult.output || "No analysis output"}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </>
                        ) : (
                            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
                                <div className="w-16 h-16 text-gray-400 mx-auto mb-4">
                                    <Code />
                                </div>
                                <h3 className="text-lg font-semibold text-gray-900 mb-2">No Analysis Yet</h3>
                                <p className="text-gray-600">
                                    Upload or paste your code and click "Analyze Code" to get started
                                </p>
                            </div>
                        )}
                    </div>
                </div>
                )}
            </main>
        </div>
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<CodeSenseAI />);