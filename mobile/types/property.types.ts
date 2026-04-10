export type PropertyType = "house" | "apartment" | "land" | "commercial" | "office";
export type PropertyStatus = "active" | "paused" | "sold" | "rented";
export type PropertyOperation = "sale" | "rent";

export interface Property {
  id: string;
  agent_id: string;
  title: string;
  description: string | null;
  price: number;
  currency: string;
  type: PropertyType | null;
  status: PropertyStatus;
  operation: PropertyOperation | null;
  address: string;
  city: string | null;
  state: string | null;
  zip_code: string | null;
  latitude: number | null;
  longitude: number | null;
  bedrooms: number;
  bathrooms: number;
  area_m2: number | null;
  parking_spots: number;
  year_built: number | null;
  amenities: string[] | null;
  images: string[] | null;
  virtual_tour_url: string | null;
  is_featured: boolean;
  views_count: number;
  created_at: string;
  updated_at: string;
}

export interface PropertyFilters {
  operation?: PropertyOperation;
  type?: PropertyType;
  city?: string;
  min_price?: number;
  max_price?: number;
  min_bedrooms?: number;
  min_bathrooms?: number;
  min_area?: number;
  page?: number;
  limit?: number;
}
