import React, { lazy, Suspense } from 'react';
import './LandingPage.css';

const Globe = lazy(() => import('../Globe/Globe'));

const LandingPage = ({ onGetStarted }) => {
  return (
    <div className="landing-page">
      <div className="landing-content">
        <h1 className="landing-title">C O D E X</h1>
        <p className="landing-subtitle">Offline Medical Translation Services</p>
        <p className="landing-description">
          Translate medicine names across regions worldwide
        </p>
        <button className="get-started-btn" onClick={onGetStarted}>
          GET STARTED
        </button>
        <div className="landing-globe">
          <Suspense fallback={<div className="globe-placeholder" />}>
            <Globe mini={true} />
          </Suspense>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
