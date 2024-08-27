"use client"

import { useState, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import Image from 'next/image'

export default function Home() {
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResult, setSearchResult] = useState('')
  const [meetingLink, setMeetingLink] = useState('')
  const [animationOffset, setAnimationOffset] = useState(0)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [isSearchLoading, setIsSearchLoading] = useState(false)

  useEffect(() => {
    const intervalId = setInterval(() => {
      setAnimationOffset((prev) => (prev + 1) % 100)
    }, 50)
    return () => clearInterval(intervalId)
  }, [])

  const handleSearch = async () => {
    setIsSearchLoading(true)
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
      setIsSearchLoading(false)
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
    <div className="min-h-screen bg-[#f5f5f1] text-gray-900 font-sans">
      <header className="bg-white shadow-sm relative overflow-hidden">
        <div className="container mx-auto px-4 py-20 text-center relative z-10">
          <h1 className="text-6xl font-bold mb-12">Get to know Akhilesh.</h1>
          <div className="w-64 h-64 mx-auto mb-12 rounded-full overflow-hidden shadow-lg relative">
            <div 
              className="absolute inset-0 bg-gradient-to-r from-blue-400 to-purple-500 opacity-20"
              style={{
                backgroundImage: `repeating-linear-gradient(
                  45deg,
                  transparent,
                  transparent 10px,
                  rgba(255,255,255,0.1) 10px,
                  rgba(255,255,255,0.1) 20px
                )`,
                backgroundSize: '141% 141%',
                backgroundPosition: `${animationOffset}% ${animationOffset}%`,
                transition: 'background-position 0.5s ease-out'
              }}
            ></div>
            <Image 
              src="/akhilesh-profile.jpg" 
              alt="Akhilesh's profile" 
              width={256} 
              height={256}
              className="object-cover relative z-10"
            />
          </div>
        </div>
        <div 
          className="absolute inset-0 bg-gradient-to-r from-blue-400 to-purple-500 opacity-10"
          style={{
            backgroundImage: `repeating-linear-gradient(
              45deg,
              transparent,
              transparent 20px,
              rgba(255,255,255,0.1) 20px,
              rgba(255,255,255,0.1) 40px
            )`,
            backgroundSize: '200% 200%',
            backgroundPosition: `${animationOffset}% ${animationOffset}%`,
            transition: 'background-position 0.5s ease-out'
          }}
        ></div>
      </header>

      <main className="container mx-auto px-4 py-16 max-w-3xl">
        <section className="mb-16">
          <h2 className="text-3xl font-semibold mb-6">Embedding Search Engine</h2>
          <p className="mb-6 text-gray-600">Ask about Akhilesh and get instant answers.</p>
          <div className="space-y-4">
            <Input
              type="text"
              placeholder="What would you like to know?"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full border-gray-300 rounded-full py-3 px-6 text-lg"
            />
            <Button 
              onClick={handleSearch} 
              disabled={isSearchLoading}
              className="w-full bg-gray-900 text-white hover:bg-gray-800 rounded-full py-3 text-lg"
            >
              {isSearchLoading ? 'Searching...' : 'Search'}
            </Button>
          </div>
          {isSearchLoading && (
            <div className="mt-6 p-6 bg-white rounded-lg shadow-sm">
              <p className="text-gray-800">Searching...</p>
            </div>
          )}
          {searchResult && (
            <div className="mt-6 p-6 bg-white rounded-lg shadow-sm">
              <p className="text-gray-800">{searchResult}</p>
            </div>
          )}
        </section>

        <section>
          <h2 className="text-3xl font-semibold mb-6">AI Clone Meeting</h2>
          <p className="mb-6 text-gray-600">Get to know Akhilesh better through an AI-powered meeting.</p>
          <Button 
            onClick={handleMeeting} 
            disabled={isLoading}
            className="w-full bg-gray-900 text-white hover:bg-gray-800 rounded-full py-3 text-lg"
          >
            {isLoading ? 'Creating Meeting...' : 'Create Meeting'}
          </Button>
          {isLoading && (
            <div className="mt-6 p-6 bg-white rounded-lg shadow-sm">
              <p className="text-gray-800">Creating meeting link...</p>
            </div>
          )}
          {error && (
            <div className="mt-6 p-6 bg-white rounded-lg shadow-sm">
              <p className="text-red-600">{error}</p>
            </div>
          )}
          {meetingLink && (
            <div className="mt-6 p-6 bg-white rounded-lg shadow-sm">
              <p className="text-gray-800">Your meeting link: <a href={meetingLink} className="text-blue-600 hover:underline">{meetingLink}</a></p>
            </div>
          )}
        </section>
      </main>

      <footer className="bg-white mt-16 py-8 text-center text-gray-600">
        <p>&copy; {new Date().getFullYear()} Akhilesh. All rights reserved.</p>
      </footer>
    </div>
  )
}