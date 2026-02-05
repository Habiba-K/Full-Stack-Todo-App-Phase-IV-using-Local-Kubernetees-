---
name: frontend-skill
description: Build pages, components, layouts, and styling for responsive and modern web applications. Use for React and Next.js development.
---

# Frontend Skill – Pages, Components, Layout, Styling

## Instructions

1. **Page & Layout Structure**
   - Design responsive page layouts that adapt to different screen sizes  
   - Organize pages with reusable layout components (headers, footers, grids)  
   - Use semantic HTML elements for better accessibility  

2. **Component Creation**
   - Build modular, reusable React components  
   - Pass data through props and manage component state efficiently  
   - Use component composition for flexibility and maintainability  

3. **Styling**
   - Apply CSS, Tailwind, or styled-components for consistent styling  
   - Maintain responsive design using media queries or utility classes  
   - Implement visual hierarchy and spacing for clarity  
   - Support dark/light modes if needed  

4. **Interactivity**
   - Add animations, transitions, and micro-interactions  
   - Handle user events like clicks, forms, and keyboard input  
   - Ensure accessibility standards (ARIA attributes, keyboard navigation)  

## Best Practices
- Keep components small and single-purpose  
- Follow naming conventions for files, components, and classes  
- Avoid inline styles where reusable classes or styled-components work better  
- Optimize rendering performance and minimize unnecessary re-renders  
- Test components across browsers and devices  

## Example Structure
```jsx
// Layout Component
export default function Layout({ children }) {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-blue-600 text-white p-4">Header</header>
      <main className="flex-1 p-4">{children}</main>
      <footer className="bg-gray-200 text-center p-4">Footer</footer>
    </div>
  );
}

// Page Component
export default function HomePage() {
  return (
    <Layout>
      <section className="text-center py-20">
        <h1 className="text-4xl font-bold">Welcome to the App</h1>
        <p className="mt-4 text-lg">Build responsive, interactive pages with ease.</p>
      </section>
    </Layout>
  );
}
