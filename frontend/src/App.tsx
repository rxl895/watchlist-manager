import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Toaster } from 'react-hot-toast';
import { ThemeProvider } from 'styled-components';
import { GlobalStyles, theme } from './styles/GlobalStyles';
import Header from './components/Layout/Header';
import Sidebar from './components/Layout/Sidebar';
import Dashboard from './pages/Dashboard';
import Watchlist from './pages/Watchlist';
import Analytics from './pages/Analytics';
import Recommendations from './pages/Recommendations';
import Search from './pages/Search';
import ContentDetail from './pages/ContentDetail';
import { Layout, MainContent } from './styles/LayoutStyles';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <GlobalStyles />
        <Router>
          <Layout>
            <Header />
            <div style={{ display: 'flex', flex: 1 }}>
              <Sidebar />
              <MainContent>
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/watchlist" element={<Watchlist />} />
                  <Route path="/analytics" element={<Analytics />} />
                  <Route path="/recommendations" element={<Recommendations />} />
                  <Route path="/search" element={<Search />} />
                  <Route path="/content/:id" element={<ContentDetail />} />
                </Routes>
              </MainContent>
            </div>
          </Layout>
        </Router>
        <Toaster position="top-right" />
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;
