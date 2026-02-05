'use client';

import { ReactNode } from 'react';

interface AnimatedSectionProps {
  children: ReactNode;
  delay?: number;
  className?: string;
}

export default function AnimatedSection({
  children,
  delay,
  className = ''
}: AnimatedSectionProps) {
  // Map delay values to CSS classes
  const getDelayClass = () => {
    if (!delay) return '';
    if (delay === 100) return 'animation-delay-100';
    if (delay === 200) return 'animation-delay-200';
    if (delay === 300) return 'animation-delay-300';
    return '';
  };

  const delayClass = getDelayClass();
  const animationClasses = `animate-fade-in-up ${delayClass}`.trim();

  return (
    <div className={`${animationClasses} ${className}`.trim()}>
      {children}
    </div>
  );
}
