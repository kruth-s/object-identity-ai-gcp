export interface AnalysisResult {
  request_id: string;
  timestamp: number;
  normalized_gcs_uri: string;
  fusion_summary: {
    confidence: number;
    branch_weights: Record<string, number>;
  };
  branch_confidences: Record<string, number>;
  explainability: {
    summary: string;
    heatmap_object_path: string;
  };
  top_k: Array<{
    object_id: string;
    score: number;
  }>;
}

export interface LocationData {
  street_area: string;
  pin_code: string;
  city: string;
  state: string;
  country?: string;
}

export interface ContactData {
  phone: string;
  email: string;
}

export interface ItemCreate {
  name: string;
  category: string;
  description: string;
  date_time: string; // ISO string
  status: "Lost" | "Found";
  location: LocationData;
  contact: ContactData;
  images: string[];
}

export interface ItemResponse {
  message: string;
  id: string;
}

const getApiUrl = () => {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  if (!apiUrl) {
    throw new Error("NEXT_PUBLIC_API_URL is not defined in environment variables");
  }
  return apiUrl;
};

export const analyzeImage = async (file: File): Promise<AnalysisResult> => {
  const apiUrl = getApiUrl();
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${apiUrl}/analyze`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Analysis failed: ${response.status} ${response.statusText} - ${errorText}`);
  }

  return response.json();
};

export const createItem = async (data: ItemCreate): Promise<ItemResponse> => {
  const apiUrl = getApiUrl();
  
  const response = await fetch(`${apiUrl}/upload`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Item creation failed: ${response.status} ${response.statusText} - ${errorText}`);
  }

  return response.json();
};
