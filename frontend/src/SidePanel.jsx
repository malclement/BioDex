import { useState } from 'react';
import './SidePanel.css';

const SidePanel = () => {
  const [isCollapsed, setIsCollapsed] = useState(false);

  const togglePanel = () => {
    setIsCollapsed(!isCollapsed);
  };

  return (
    <div className="side-panel-container">
      <div className={`side-panel ${isCollapsed ? 'collapsed' : ''}`}>
        <div className="panel-content">
          {/* Panel content will be added later */}
        </div>
      </div>
      <button
        className="collapse-button"
        onClick={togglePanel}
        aria-label={isCollapsed ? 'Expand panel' : 'Collapse panel'}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          fill="currentColor"
          viewBox="0 0 16 16"
          style={{ transform: isCollapsed ? 'rotate(180deg)' : 'none', transition: 'transform 0.3s' }}
        >
          <path fillRule="evenodd" d="M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0z"/>
        </svg>
      </button>
    </div>
  );
};

export default SidePanel;
