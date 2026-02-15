import React, { useState } from 'react';
import { 
  Plus, MessageSquare, Trash2, LayoutDashboard, 
  Library, Share2, Settings, ChevronDown, Search,
  Compass, Zap, History, X
} from 'lucide-react';

export default function Sidebar({ allChats, activeChatId, loadChat, deleteChat, handleNewChat, user }) {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [isHistoryExpanded, setIsHistoryExpanded] = useState(true);

  return (
    <div className={`sidebar-wrapper ${isCollapsed ? 'collapsed' : ''}`}>
      {/* LEFT SLIM RAIL: Permanent icons */}
      <aside className="icon-rail">
        <div className="rail-top">
          <div className="rail-logo">
             <Zap size={22} className="text-blue-500" fill="currentColor" />
          </div>
          <div className="rail-icon active" onClick={() => setIsCollapsed(!isCollapsed)}>
            <LayoutDashboard size={20} />
          </div>
          <div className="rail-icon"><Compass size={20} /></div>
          <div className="rail-icon"><Library size={20} /></div>
        </div>
        <div className="rail-bottom">
          <div className="rail-icon"><Settings size={20} /></div>
        </div>
      </aside>

      {/* MAIN NAV PANEL: The expandable/collapsible part */}
      <aside className="nav-panel glass">
        <div className="mac-controls">
          <span className="dot close"></span>
          <span className="dot minimize"></span>
          <span className="dot maximize"></span>
        </div>

        <div className="profile-section-mini">
          <div className="avatar-circle">{user.name.charAt(0)}</div>
          <div className="user-text">
            <p className="name-label">{user.name}</p>
            <p className="email-label">{user.email}</p>
          </div>
        </div>

        <button className="new-project-btn" onClick={handleNewChat}>
          <Plus size={16} /> New Project
        </button>

        <div className="nav-scroll">
          <div className="nav-group">
            <div className="group-header">HISTORY</div>
            <div className="history-container">
              {allChats.map(chat => (
                <div 
                  key={chat.id} 
                  className={`history-pill group ${activeChatId === chat.id ? 'active' : ''}`}
                  onClick={() => loadChat(chat)}
                >
                  <MessageSquare size={14} className="opacity-50" />
                  <span className="pill-text">{chat.title}</span>
                  <button 
                    className="delete-pill-btn"
                    onClick={(e) => deleteChat(e, chat.id)}
                  >
                    <X size={12} />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      </aside>
    </div>
  );
}