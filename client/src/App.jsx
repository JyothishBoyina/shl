import { useState, useEffect } from 'react'
import { Search, Sparkles, Clock, Globe, BookOpen, Monitor, Moon, Sun, History, Filter, X } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"

function App() {
    const [query, setQuery] = useState('')
    const [results, setResults] = useState([])
    const [filteredResults, setFilteredResults] = useState([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [useAI, setUseAI] = useState(true)

    // Theme State
    const [theme, setTheme] = useState(() => {
        if (typeof window !== 'undefined' && window.localStorage) {
            return localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
        }
        return 'dark' // default
    })

    // History State
    const [history, setHistory] = useState(() => {
        if (typeof window !== 'undefined' && window.localStorage) {
            try {
                return JSON.parse(localStorage.getItem('searchHistory')) || []
            } catch {
                return []
            }
        }
        return []
    })

    // Filters State
    const [filters, setFilters] = useState({
        jobLevel: 'All',
        duration: 'All',
        testType: 'All'
    })

    // Theme Effect
    useEffect(() => {
        const root = window.document.documentElement
        root.classList.remove('light', 'dark')
        root.classList.add(theme)
        localStorage.setItem('theme', theme)
    }, [theme])

    const toggleTheme = () => {
        setTheme(prev => prev === 'dark' ? 'light' : 'dark')
    }

    // Save History
    const addToHistory = (text) => {
        setHistory(prev => {
            const newHistory = [text, ...prev.filter(h => h !== text)].slice(0, 5)
            localStorage.setItem('searchHistory', JSON.stringify(newHistory))
            return newHistory
        })
    }

    const clearHistory = () => {
        setHistory([])
        localStorage.removeItem('searchHistory')
    }

    const handleSearch = async (textOverride = null) => {
        const searchText = textOverride || query
        if (!searchText.trim()) return

        // Update query if using history
        if (textOverride) setQuery(textOverride)

        setLoading(true)
        setError(null)
        setResults([])
        setFilteredResults([])

        try {
            const response = await fetch('/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: searchText, use_ai: useAI }),
            })

            if (!response.ok) {
                throw new Error('Failed to fetch recommendations')
            }

            const data = await response.json()
            setResults(data)
            setFilteredResults(data) // Initial full list
            addToHistory(searchText)
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleSearch()
        }
    }

    // Filter Logic
    useEffect(() => {
        let res = [...results]

        if (filters.jobLevel !== 'All') {
            res = res.filter(item => item.job_level && item.job_level.toLowerCase().includes(filters.jobLevel.toLowerCase()))
        }

        if (filters.duration !== 'All') {
            res = res.filter(item => item.duration && item.duration.includes(filters.duration))
        }

        if (filters.testType !== 'All') {
            res = res.filter(item => item.test_type && item.test_type === filters.testType)
        }

        setFilteredResults(res)
    }, [filters, results])

    return (
        <div className="min-h-screen bg-background text-foreground font-sans selection:bg-primary/20 transition-colors duration-300">
            {/* Header */}
            <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
                <div className="container flex h-16 items-center space-x-4 sm:justify-between sm:space-x-0">
                    <div className="flex gap-2 items-center font-bold text-xl tracking-tighter">
                        <div className="bg-primary text-primary-foreground p-1 rounded-lg">
                            <Sparkles className="h-5 w-5" />
                        </div>
                        <span>TalentLens AI</span>
                    </div>
                    <div className="flex flex-1 items-center justify-end space-x-4">
                        <nav className="flex items-center space-x-2">
                            <Button variant="ghost" size="icon" onClick={toggleTheme}>
                                {theme === 'dark' ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
                            </Button>
                            <Button variant="ghost" size="sm">Documentation</Button>
                        </nav>
                    </div>
                </div>
            </header>

            <main className="container py-10 md:py-20 space-y-12">

                {/* Hero / Search Section */}
                <section className="flex flex-col items-center text-center space-y-6 max-w-3xl mx-auto">
                    <h1 className="text-4xl md:text-6xl font-black tracking-tight lg:leading-[1.1]">
                        Find the perfect <span className="text-primary bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-violet-600">SHL Assessment</span>
                    </h1>
                    <p className="text-muted-foreground text-lg md:text-xl max-w-[85%] leading-normal">
                        AI-powered recommendations tailored to your job descriptions.
                        Reduce hiring time by 80% with precise matching.
                    </p>

                    <div className="w-full max-w-2xl flex gap-2 items-center p-2 rounded-xl border bg-card shadow-lg mt-8 transition-all focus-within:ring-2 ring-primary/20">
                        <Search className="ml-3 h-5 w-5 text-muted-foreground" />
                        <Input
                            className="border-0 shadow-none focus-visible:ring-0 text-lg py-6"
                            placeholder="Describe the role... (e.g. Senior Java Developer with AWS)"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            onKeyDown={handleKeyPress}
                        />
                        <Button
                            size="lg"
                            onClick={() => handleSearch()}
                            disabled={loading}
                            className="bg-gradient-to-r from-blue-600 to-violet-600 hover:from-blue-700 hover:to-violet-700 transition-all font-semibold"
                        >
                            {loading ? (
                                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                            ) : (
                                "Search"
                            )}
                        </Button>
                    </div>

                    {/* Search History */}
                    {history.length > 0 && (
                        <div className="flex flex-wrap items-center justify-center gap-2 mt-4 animate-in fade-in zoom-in duration-300">
                            <span className="text-xs text-muted-foreground uppercase tracking-wider font-semibold flex items-center gap-1">
                                <History className="h-3 w-3" /> Recent:
                            </span>
                            {history.map((h, i) => (
                                <Button
                                    key={i}
                                    variant="secondary"
                                    size="sm"
                                    className="h-7 text-xs rounded-full px-3 hover:bg-primary hover:text-primary-foreground transition-colors"
                                    onClick={() => handleSearch(h)}
                                >
                                    {h}
                                </Button>
                            ))}
                            <Button variant="ghost" size="icon" className="h-6 w-6 rounded-full opacity-50 hover:opacity-100" onClick={clearHistory}>
                                <X className="h-3 w-3" />
                            </Button>
                        </div>
                    )}
                </section>

                {/* Filters & Results */}
                {results.length > 0 && (
                    <section className="animate-in fade-in slide-in-from-bottom-8 duration-700 space-y-6">

                        {/* Filter Bar */}
                        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-4 border rounded-xl bg-card/50 backdrop-blur-sm">
                            <div className="flex items-center gap-2 font-semibold">
                                <Filter className="h-4 w-4 text-primary" />
                                Filters
                            </div>

                            <div className="flex flex-wrap gap-3">
                                {/* Job Level Filter */}
                                <div className="flex items-center gap-2">
                                    <label className="text-xs text-muted-foreground font-medium">Level</label>
                                    <select
                                        className="h-8 rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                                        value={filters.jobLevel}
                                        onChange={(e) => setFilters({ ...filters, jobLevel: e.target.value })}
                                    >
                                        <option value="All">All Levels</option>
                                        <option value="Entry">Entry Level</option>
                                        <option value="Graduate">Graduate</option>
                                        <option value="Senior">Senior / Experienced</option>
                                        <option value="Manager">Manager / Executive</option>
                                    </select>
                                </div>

                                {/* Test Type Filter */}
                                <div className="flex items-center gap-2">
                                    <label className="text-xs text-muted-foreground font-medium">Type</label>
                                    <select
                                        className="h-8 rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                                        value={filters.testType}
                                        onChange={(e) => setFilters({ ...filters, testType: e.target.value })}
                                    >
                                        <option value="All">All Types</option>
                                        <option value="Assessment">Assessment</option>
                                        <option value="Personality">Personality</option>
                                        <option value="Cognitive">Cognitive</option>
                                        <option value="Skill">Skill Test</option>
                                    </select>
                                </div>
                            </div>
                        </div>

                        <div className="flex items-center justify-between">
                            <h2 className="text-2xl font-bold tracking-tight">Recommended Assessments</h2>
                            <span className="text-muted-foreground">{filteredResults.length} matches found</span>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {filteredResults.map((item, idx) => (
                                <Card key={idx} className="group relative overflow-hidden border-muted-foreground/20 hover:border-primary/50 transition-all duration-300 hover:shadow-xl hover:-translate-y-1 bg-gradient-to-br from-card to-secondary/20">
                                    <div className={`absolute top-0 right-0 p-3 bg-gradient-to-bl ${idx < 3 ? 'from-green-500/20 text-green-700 dark:text-green-400' : 'from-blue-500/10 text-blue-600'} rounded-bl-xl text-xs font-bold`}>
                                        {(item.score * 100).toFixed(0)}% Match
                                    </div>

                                    <CardHeader>
                                        <CardTitle className="leading-snug pr-8 text-xl min-h-[3.5rem] flex items-center">
                                            <a href={item.url} target="_blank" rel="noreferrer" className="hover:underline decoration-primary/50 underline-offset-4">
                                                {item.name}
                                            </a>
                                        </CardTitle>
                                        <CardDescription className="line-clamp-2 min-h-[2.5rem]">
                                            {item.description}
                                        </CardDescription>
                                    </CardHeader>

                                    <CardContent className="space-y-4">
                                        {/* Metadata grid */}
                                        <div className="grid grid-cols-2 gap-3 text-sm">
                                            <div className="flex items-center gap-2 text-muted-foreground bg-secondary/50 p-2 rounded">
                                                <Clock className="h-4 w-4 text-primary" />
                                                <span>{item.duration || 'N/A'}</span>
                                            </div>
                                            <div className="flex items-center gap-2 text-muted-foreground bg-secondary/50 p-2 rounded">
                                                <BookOpen className="h-4 w-4 text-primary" />
                                                <span className="truncate">{item.job_level || 'Any Level'}</span>
                                            </div>
                                        </div>

                                        {/* AI Insights (Top 3 only typically) */}
                                        {item.ai_insights && (
                                            <div className="mt-4 p-3 bg-primary/5 border border-primary/10 rounded-lg text-sm text-foreground/90 relative overflow-hidden">
                                                <div className="absolute top-0 left-0 w-1 h-full bg-gradient-to-b from-blue-500 to-violet-500"></div>
                                                <div className="flex items-center gap-2 mb-2 font-semibold text-primary">
                                                    <Sparkles className="h-3 w-3" /> AI Analysis
                                                </div>
                                                <div className="prose prose-sm max-w-none text-muted-foreground text-xs leading-relaxed whitespace-pre-wrap">
                                                    {item.ai_insights}
                                                </div>
                                            </div>
                                        )}
                                    </CardContent>

                                    <CardFooter className="pt-2">
                                        <Button variant="outline" className="w-full group-hover:bg-primary group-hover:text-primary-foreground transition-colors" asChild>
                                            <a href={item.url} target="_blank" rel="noreferrer">
                                                View Details
                                            </a>
                                        </Button>
                                    </CardFooter>
                                </Card>
                            ))}

                            {filteredResults.length === 0 && (
                                <div className="col-span-full py-12 text-center text-muted-foreground border-2 border-dashed rounded-xl">
                                    <p>No results match your filters.</p>
                                    <Button variant="link" onClick={() => setFilters({ jobLevel: 'All', duration: 'All', testType: 'All' })}>
                                        Clear Filters
                                    </Button>
                                </div>
                            )}
                        </div>
                    </section>
                )}
            </main>
        </div>
    )
}

export default App
