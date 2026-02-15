// File Path: frontend/src/App.jsx
import React, { useState, useRef, useEffect } from 'react';
import { 
  LayoutDashboard, Share2, Plus, MessageSquare, 
  Settings, Send, Sparkles, Trash2, Menu, ChevronLeft, HelpCircle, CheckCircle2 
} from 'lucide-react';
import './App.css';

export default function App() {
  // --- Profile State ---
  const [user, setUser] = useState({ name: "John Doe", email: "PRO MEMB" });
  const [tempUser, setTempUser] = useState({ ...user });
  const [isEditing, setIsEditing] = useState(false);

  // --- UI & Chat State ---
  const [input, setInput] = useState("");
  const [isChatting, setIsChatting] = useState(false);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [history, setHistory] = useState([]);

  const chatEndRef = useRef(null);

  const templates = [
    { icon: "🚀", title: "Hackathon", text: "Build a real-time collaborative coding platform" },
    { icon: "🛠️", title: "MVP", text: "Create a subscription-based meal planning app" },
    { icon: "📱", title: "Product", text: "Launch a B2B SaaS platform for content" }
  ];

  const getInitials = (name) => name.substring(0, 2).toUpperCase();

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSaveProfile = () => {
    setUser(tempUser);
    setIsEditing(false);
  };

  const handleCancelProfile = () => {
    setTempUser(user);
    setIsEditing(false);
  };

  // --- Updated Backend Integration (Dynamic Chat) ---
  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    if (!input.trim()) return;

    const userText = input;
    const userMsg = { id: Date.now(), role: 'user', text: userText };
    setMessages(prev => [...prev, userMsg]);
    setIsChatting(true);
    setInput("");
    setLoading(true);

    try {
      // Prepare history to send to Groq (last 10 messages)
      const chatHistory = messages.map(m => ({
        role: m.role === 'ai' ? 'assistant' : 'user',
        content: m.text
      })).slice(-10);

      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: JSON.stringify({
          message: userText,
          history: chatHistory
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Internal Server Error");
      }

      // Handle structured response with phases
      if (data.phases && data.phases.length > 0) {
        let formattedText = data.reply + "\n\n";
        data.phases.forEach(phase => {
          formattedText += `\n📋 Phase ${phase.number}: ${phase.name}\n`;
          formattedText += `Status: ${phase.status === 'active' ? '⚡ Active' : '⏳ Pending'}\n`;
          formattedText += `\nTasks:\n`;
          phase.tasks.forEach((task, i) => {
            formattedText += `  ${i+1}. ☐ ${task}\n`;
          });
          formattedText += `\n✅ Commit: ${phase.commit_msg}\n`;
        });
        
        setMessages(prev => [...prev, { 
          id: Date.now() + 1, 
          role: 'ai', 
          text: formattedText,
          phases: data.phases
        }]);
      } else {
        setMessages(prev => [...prev, { 
          id: Date.now() + 1, 
          role: 'ai', 
          text: data.reply
        }]);
      }

      // Add to sidebar history if it's a new conversation
      if (messages.length === 0) {
        setHistory(prev => [{ id: Date.now(), title: userText.substring(0, 24) + "..." }, ...prev]);
      }

    } catch (err) {
      console.error("Fetch failure:", err);
      console.error("Error stack:", err.stack);
      setMessages(prev => [...prev, { 
        id: Date.now() + 1, 
        role: 'ai', 
        isError: true,
        text: `Backend Error: ${err.message}` 
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`gemini-layout ${isSidebarCollapsed ? 'collapsed' : 'expanded'}`}>
      
      {/* SIDEBAR */}
      <aside className="sidebar glass-effect">
        <div className="sidebar-header-top">
          <button className="toggle-btn-top" onClick={() => setIsSidebarCollapsed(!isSidebarCollapsed)}>
            {isSidebarCollapsed ? <Menu size={24} /> : <ChevronLeft size={24} />}
          </button>
          
          <div className="profile-section">
            <div className="avatar">{getInitials(user.name)}</div>
            {!isSidebarCollapsed && (
              <div className="user-info">
                {isEditing ? (
                  <div className="edit-mini-form">
                    <input 
                      className="edit-input"
                      value={tempUser.name} 
                      onChange={(e) => setTempUser({...tempUser, name: e.target.value})}
                      autoFocus
                    />
                    <div className="edit-btns">
                      <button onClick={handleSaveProfile}>OK</button>
                      <button onClick={handleCancelProfile}>Cancel</button>
                    </div>
                  </div>
                ) : (
                  <>
                    <div className="user-name">{user.name}</div>
                    <div className="user-status">{user.email}</div>
                  </>
                )}
              </div>
            )}
          </div>
        </div>

        <button className="new-chat-btn" onClick={() => {setIsChatting(false); setMessages([]);}}>
          <Plus size={20} />
          {!isSidebarCollapsed && <span>New Project</span>}
        </button>

        <nav className="nav-container">
          <div className="nav-item"><LayoutDashboard size={20} /> {!isSidebarCollapsed && <span>Dashboard</span>}</div>
          <div className="nav-item"><Share2 size={20} /> {!isSidebarCollapsed && <span>Share</span>}</div>
        </nav>

        <div className="history-section no-scrollbar">
          {!isSidebarCollapsed && history.length > 0 && <div className="history-header">RECENT</div>}
          <div className="history-list">
            {history.map(chat => (
              <div key={chat.id} className="history-pill chat-entry-anim">
                <MessageSquare size={18} />
                {!isSidebarCollapsed && (
                  <>
                    <span className="chat-title-text">{chat.title}</span>
                    <button className="delete-chat-btn" onClick={(e) => {
                      e.stopPropagation();
                      setHistory(prev => prev.filter(h => h.id !== chat.id));
                    }}><Trash2 size={14} /></button>
                  </>
                )}
              </div>
            ))}
          </div>
        </div>

        <div className="sidebar-footer">
          <div className="nav-item"><HelpCircle size={20} /> {!isSidebarCollapsed && <span>Help</span>}</div>
          <div className="nav-item" onClick={() => setIsEditing(true)}>
            <Settings size={20} />
            {!isSidebarCollapsed && <span>Settings</span>}
          </div>
        </div>
      </aside>

      {/* MAIN CONTENT */}
      <main className="main-content">
        <header className="brand-title-center">EXECUTION ORACLE v3.0</header>
        
        <div className="chat-scroll-area no-scrollbar">
          {!isChatting ? (
            <div className="hero-box">
              <h1 className="hero-title">
                <span className="text-fade">What will you</span><br/>
                <span className="gradient-text">Build Today?</span>
              </h1>

              <div className="features-row">
                <div className="feature-mini-card glass-effect border-blue">
                  <div className="icon-wrap blue-glow"><Sparkles size={22}/></div>
                  <div className="f-label color-blue">Smart Decomposition</div>
                  <div className="f-sub">AI breaks ideas into phases.</div>
                </div>
                <div className="feature-mini-card glass-effect border-purple">
                  <div className="icon-wrap purple-glow"><Sparkles size={22}/></div>
                  <div className="f-label color-purple">Scope Detection</div>
                  <div className="f-sub">Real-time timeline alerts.</div>
                </div>
                <div className="feature-mini-card glass-effect border-red">
                  <div className="icon-wrap red-glow"><Sparkles size={22}/></div>
                  <div className="f-label color-red">Adaptive Guidance</div>
                  <div className="f-sub">Progress-based tips.</div>
                </div>
              </div>
            </div>
          ) : (
            <div className="chat-container">
              {messages.map(m => (
                <div key={m.id} className={`message-bubble-wrapper ${m.role}`}>
                  <div className={`message-bubble glass-effect ${m.role === 'ai' ? 'ai-glow' : ''} ${m.isError ? 'error-bubble' : ''}`}>
                    {/* Render text with preserved line breaks for folder structures */}
                    <div style={{ whiteSpace: 'pre-wrap' }}>{m.text}</div>
                    
                    {m.phases && (
                      <div className="phases-list">
                        {m.phases.map((phase, i) => (
                          <div key={i} className="phase-card">
                            <CheckCircle2 size={16} className="phase-icon" />
                            <span>Phase {phase.number}: {phase.name}</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))}
              {loading && (
                <div className="message-bubble-wrapper ai">
                  <div className="message-bubble glass-effect shimmer-blink">
                    <Sparkles size={18} className="blink-icon" /> Oracle is thinking...
                  </div>
                </div>
              )}
              <div ref={chatEndRef} />
            </div>
          )}
        </div>

        <div className="bottom-controls">
          <div className="input-wrapper">
            <form className="search-box glass-effect" onSubmit={handleSubmit}>
              <input 
                type="text" 
                placeholder="Describe your project idea..." 
                value={input}
                onChange={(e) => setInput(e.target.value)}
              />
              <button type="submit" className="send-btn-neon">
                <Send size={24} strokeWidth={2.5} />
              </button>
            </form>
            
            {!isChatting && (
              <div className="template-row no-scrollbar">
                {templates.map((t, idx) => (
                  <button key={idx} onClick={() => setInput(t.text)} className="template-pill glass-effect">
                    {t.icon} {t.title}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}