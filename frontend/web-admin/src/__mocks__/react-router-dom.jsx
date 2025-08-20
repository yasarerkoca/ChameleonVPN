import React from 'react';

export const BrowserRouter = ({ children }) => <div>{children}</div>;
export const Routes = ({ children }) => <div>{children}</div>;
export const Route = ({ element }) => <>{element}</>;
export const Link = ({ to, children }) => <a href={to}>{children}</a>;
