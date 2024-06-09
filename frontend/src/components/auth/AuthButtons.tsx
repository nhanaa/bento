import { AuthButton } from "./AuthButton";


export const AuthButtons = () => {
    return (
      <div className="flex flex-col gap-1">
        <AuthButton
          brand="google"
          imgUrl={
            "https://cdn.iconscout.com/icon/free/png-256/free-google-1772223-1507807.png"
          }
        />
      </div>
    );
}