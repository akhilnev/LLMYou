"use client"

import { useState, useEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import Image from 'next/image'
import { FaLinkedin, FaTwitter, FaEnvelope, FaSearch, FaVideo, FaBriefcase /* , FaFileAlt */ } from 'react-icons/fa'
import WorkTimeline from '@/components/ui/WorkTimeLine'


export default function Home() {
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResult, setSearchResult] = useState('')
  const [meetingLink, setMeetingLink] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [activeSection, setActiveSection] = useState<'search' | 'meeting' | 'timeline' /* | 'resume' */ | null>(null)

  const handleSearch = async () => {
    setIsLoading(true)
    setSearchResult('')
    try {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: searchQuery }),
      })
      const data = await response.json()
      setSearchResult(data.result)
    } catch (error) {
      console.error('Error fetching search results:', error)
      setSearchResult('An error occurred while fetching results.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleMeeting = async () => {
    setIsLoading(true)
    setError('')
    setMeetingLink('')
    try {
      const response = await fetch('/api/meeting', { method: 'POST' })
      const data = await response.json()
      if (data.error) throw new Error(data.error)
      setMeetingLink(data.meetingLink)
    } catch (error) {
      console.error('Error creating meeting:', error)
      setError('An error occurred while creating the meeting.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen w-full bg-cream text-gray-900 font-sans flex flex-col items-center justify-center p-4 relative overflow-hidden cursor-none">
      <CustomCursor />
      <QuoteBackground />
      
      <main className="w-full max-w-4xl z-10 relative">
        <h1 className="text-6xl font-bold mb-12 text-center text-matte-black">
          Get to know Akhilesh.
        </h1>
        
        <div className="relative group mb-12">
          <div className="w-96 h-96 mx-auto rounded-full overflow-hidden shadow-xl transition-transform duration-300 group-hover:scale-95">
            <Image 
              src="/akhilesh-profile.jpg" 
              alt="Akhilesh's profile" 
              width={384} 
              height={384}
              className="object-cover"
            />
          </div>
          
          <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            <div className="bg-matte-black bg-opacity-90 p-6 rounded-lg shadow-lg flex space-x-6">
              <Button onClick={() => setActiveSection('search')} className="flex items-center space-x-2 bg-cream text-matte-black hover:bg-gray-200">
                <FaSearch />
                <span>Search</span>
              </Button>
              <Button onClick={() => setActiveSection('timeline')} className="flex items-center space-x-2 bg-cream text-matte-black hover:bg-gray-200">
                <FaBriefcase />
                <span>Experience</span>
              </Button>
              {/* <Button onClick={() => setActiveSection('resume')} className="flex items-center space-x-2 bg-cream text-matte-black hover:bg-gray-200">
                <FaFileAlt />
                <span>Resume</span>
              </Button> */}
              <Button onClick={() => setActiveSection('meeting')} className="flex items-center space-x-2 bg-cream text-matte-black hover:bg-gray-200">
                <FaVideo />
                <span>AI Meeting</span>
              </Button>
            </div>
          </div>
        </div>

        <div className="flex justify-center space-x-8 mb-12">
          <a href="https://www.linkedin.com/in/akhilnev/" target="_blank" rel="noopener noreferrer" className="text-matte-black hover:text-gray-600 transition-colors">
            <FaLinkedin size={28} />
          </a>
          <a href="https://x.com/akhilnev" target="_blank" rel="noopener noreferrer" className="text-matte-black hover:text-gray-600 transition-colors">
            <FaTwitter size={28} />
          </a>
          <a href="mailto:akhilesh.nevatia@gmail.com" className="text-matte-black hover:text-gray-600 transition-colors">
            <FaEnvelope size={28} />
          </a>
        </div>

        {activeSection === 'search' && (
          <div className="bg-matte-black text-cream rounded-lg shadow-lg p-8 mb-8 animate-fadeIn">
            <h2 className="text-2xl font-semibold mb-4">Embedding Search Engine</h2>
            <p className="mb-4 text-gray-300">Ask about Akhilesh and get instant answers.</p>
            <div className="space-y-4">
              <Input
                type="text"
                placeholder="What would you like to know?"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-cream text-matte-black border-gray-300 rounded-full py-2 px-4 text-lg"
              />
              <Button 
                onClick={handleSearch} 
                disabled={isLoading}
                className="w-full bg-cream text-matte-black hover:bg-gray-200 rounded-full py-2 text-lg"
              >
                {isLoading ? 'Searching...' : 'Search'}
              </Button>
            </div>
            {searchResult && (
              <div className="mt-6 p-4 bg-cream text-matte-black rounded-lg">
                <p>{searchResult}</p>
              </div>
            )}
          </div>
        )}

        {activeSection === 'meeting' && (
          <div className="bg-matte-black text-cream rounded-lg shadow-lg p-8 mb-8 animate-fadeIn">
            <h2 className="text-2xl font-semibold mb-2">AI Powered Meeting</h2>
            <p className="mb-4 text-gray-300">Get to know Akhilesh better through a 2-3 minute AI-powered meeting.</p>
            <p className="mb-4 text-yellow-300 text-sm">Note: API credits may be exhausted.</p>
            <Button 
              onClick={handleMeeting} 
              disabled={isLoading}
              className="w-full bg-cream text-matte-black hover:bg-gray-200 rounded-full py-2 text-lg"
            >
              {isLoading ? 'Creating Meeting...' : 'Create Meeting'}
            </Button>
            {error && (
              <p className="mt-4 text-red-400">{error}</p>
            )}
            {meetingLink && (
              <div className="mt-4 p-4 bg-cream text-matte-black rounded-lg">
                <p>Your meeting link: <a href={meetingLink} className="text-blue-400 hover:underline">{meetingLink}</a></p>
              </div>
            )}
          </div>
        )}

        {activeSection === 'timeline' && (
          <div className="bg-matte-black text-cream rounded-lg shadow-lg p-8 mb-8 animate-fadeIn">
            <h2 className="text-2xl font-semibold mb-4">Work Experience Timeline</h2>
            <WorkTimeline />
          </div>
        )}

        {/* {activeSection === 'resume' && (
          <div className="bg-matte-black text-cream rounded-lg shadow-lg p-8 mb-8 animate-fadeIn">
            <h2 className="text-2xl font-semibold mb-4">Resume</h2>
            <div className="w-full h-[600px]">
              <iframe 
                src="https://drive.google.com/file/d/1YtHYGM9DUuHmSFnAGbEv7Ryg14qkFQUJ/preview" 
                width="100%" 
                height="100%" 
                allow="autoplay"
              ></iframe>
            </div>
          </div>
        )} */}
      </main>

      <footer className="mt-auto py-4 text-center text-matte-black relative z-10">
        <p>&copy; {new Date().getFullYear()} Akhilesh. All rights reserved.</p>
      </footer>
    </div>
  )
}

const CustomCursor = () => {
  const cursorRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const moveCursor = (e: MouseEvent) => {
      if (cursorRef.current) {
        cursorRef.current.style.left = `${e.clientX}px`
        cursorRef.current.style.top = `${e.clientY}px`
      }
    }
    window.addEventListener('mousemove', moveCursor)
    return () => window.removeEventListener('mousemove', moveCursor)
  }, [])

  return (
    <div 
      ref={cursorRef} 
      className="fixed w-8 h-8 rounded-full bg-matte-black bg-opacity-50 pointer-events-none z-50 transition-transform duration-100 ease-out"
      style={{ transform: 'translate(-50%, -50%)' }}
    />
  )
}

const QuoteBackground = () => {
  const quotes = [
    "Innovation distinguishes between a leader and a follower. - Steve Jobs",
    "The biggest risk is not taking any risk. - Mark Zuckerberg",
    "The way to get started is to quit talking and begin doing. - Walt Disney",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
    "Your time is limited, don't waste it living someone else's life. - Steve Jobs",
    "The only way to do great work is to love what you do. - Steve Jobs",
    "If you're not embarrassed by the first version of your product, you've launched too late. - Reid Hoffman",
    "The best way to predict the future is to create it. - Peter Drucker",
    "Chase the vision, not the money; the money will end up following you. - Tony Hsieh",
    "The secret to successful hiring is this: look for the people who want to change the world. - Marc Benioff",
    "We wanted flying cars, instead we got 140 characters. - Peter Thiel",
    "The most valuable businesses of coming decades will be built by entrepreneurs who seek to empower people rather than try to make them obsolete. - Peter Thiel",
    "We build technology to protect the most fundamental rights and freedoms of democratic societies. - Alex Karp",
    "The world is changing faster than ever, and the question is not whether your company will change, but how. - Alex Karp",
    "You want to be greedy when others are fearful. You want to be fearful when others are greedy. It's that simple. - Sam Altman",
    "The most successful people I know are primarily internally driven; they do what they do to impress themselves and because they feel compelled to make something happen in the world. - Sam Altman",
    "I don't believe in taking right decisions. I take decisions and then make them right. - Ratan Tata",
    "Ups and downs in life are very important to keep us going, because a straight line even in an ECG means we are not alive. - Ratan Tata"
  ];

  const fonts = [
    'serif',
    'sans-serif',
    'monospace',
    'cursive',
    'fantasy',
    'system-ui',
    'ui-serif',
    'ui-sans-serif',
    'ui-monospace',
    'ui-rounded'
  ];

  const [positions, setPositions] = useState<Array<{ x: number, y: number }>>([])

  useEffect(() => {
    const calculatePositions = () => {
      const newPositions = []
      const gridSize = Math.ceil(Math.sqrt(quotes.length))
      const cellWidth = window.innerWidth / gridSize
      const cellHeight = window.innerHeight / gridSize

      for (let i = 0; i < quotes.length; i++) {
        const row = Math.floor(i / gridSize)
        const col = i % gridSize
        newPositions.push({
          x: col * cellWidth + Math.random() * (cellWidth - 300),
          y: row * cellHeight + Math.random() * (cellHeight - 100)
        })
      }
      setPositions(newPositions)
    }

    calculatePositions()
    window.addEventListener('resize', calculatePositions)
    return () => window.removeEventListener('resize', calculatePositions)
  }, [quotes.length])

  return (
    <div className="absolute inset-0 overflow-hidden">
      {quotes.map((quote, index) => (
        <motion.div
          key={index}
          drag
          dragMomentum={false}
          initial={{ x: positions[index]?.x || 0, y: positions[index]?.y || 0, opacity: 0.7, rotate: Math.random() * 10 - 5 }}
          animate={{ x: positions[index]?.x || 0, y: positions[index]?.y || 0 }}
          whileHover={{ scale: 1.1, opacity: 1 }}
          className="absolute text-lg select-none cursor-move p-4 rounded-lg"
          style={{ 
            maxWidth: '300px', 
            textAlign: 'center',
            fontFamily: fonts[index % fonts.length],
            color: 'rgba(0, 0, 0, 0.7)',
          }}
        >
          {quote}
        </motion.div>
      ))}
    </div>
  );
};