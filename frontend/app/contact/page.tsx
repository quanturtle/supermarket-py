"use client"

import type React from "react"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Mail, MapPin, Phone } from "lucide-react"

export default function ContactPage() {
  const [formState, setFormState] = useState({
    name: "",
    email: "",
    subject: "",
    message: "",
  })

  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormState((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)

    // Simulate form submission
    setTimeout(() => {
      setIsSubmitting(false)
      setIsSubmitted(true)
      setFormState({
        name: "",
        email: "",
        subject: "",
        message: "",
      })
    }, 1500)
  }

  return (
    <>
      <h1 className="text-3xl font-bold mb-6">Contact Us</h1>

      <div className="grid gap-6 md:grid-cols-2 lg:gap-12">
        <div className="space-y-6 bg-white p-6 rounded-lg shadow-sm">
          <p className="text-lg">
            Have questions, feedback, or suggestions? We'd love to hear from you! Fill out the form and our team will
            get back to you as soon as possible.
          </p>

          <div className="space-y-4 mt-8">
            <div className="flex items-start gap-3">
              <MapPin className="h-5 w-5 text-gray-500 mt-0.5" />
              <div>
                <h3 className="font-medium">Address</h3>
                <p className="text-sm text-gray-500">
                  123 Price Comparison Street
                  <br />
                  Market District
                  <br />
                  San Francisco, CA 94103
                </p>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <Mail className="h-5 w-5 text-gray-500 mt-0.5" />
              <div>
                <h3 className="font-medium">Email</h3>
                <p className="text-sm text-gray-500">
                  info@pricetracker.example
                  <br />
                  support@pricetracker.example
                </p>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <Phone className="h-5 w-5 text-gray-500 mt-0.5" />
              <div>
                <h3 className="font-medium">Phone</h3>
                <p className="text-sm text-gray-500">
                  +1 (555) 123-4567
                  <br />
                  Mon-Fri, 9am-5pm PT
                </p>
              </div>
            </div>
          </div>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Send us a message</CardTitle>
            <CardDescription>Fill out the form below and we'll respond as soon as possible.</CardDescription>
          </CardHeader>
          <CardContent>
            {isSubmitted ? (
              <div className="flex flex-col items-center justify-center py-6 text-center">
                <h3 className="text-xl font-medium mb-2">Thank you!</h3>
                <p className="text-gray-500 mb-4">
                  Your message has been sent successfully. We'll get back to you soon.
                </p>
                <Button variant="outline" onClick={() => setIsSubmitted(false)}>
                  Send another message
                </Button>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="name">Name</Label>
                  <Input id="name" name="name" value={formState.name} onChange={handleChange} required />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    name="email"
                    type="email"
                    value={formState.email}
                    onChange={handleChange}
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="subject">Subject</Label>
                  <Input id="subject" name="subject" value={formState.subject} onChange={handleChange} required />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="message">Message</Label>
                  <Textarea
                    id="message"
                    name="message"
                    rows={5}
                    value={formState.message}
                    onChange={handleChange}
                    required
                  />
                </div>

                <Button type="submit" className="w-full" disabled={isSubmitting}>
                  {isSubmitting ? "Sending..." : "Send Message"}
                </Button>
              </form>
            )}
          </CardContent>
        </Card>
      </div>
    </>
  )
}